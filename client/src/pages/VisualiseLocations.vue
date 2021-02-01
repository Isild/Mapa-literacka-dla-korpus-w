<template>
  <v-container fill-height fluid>
    <v-row style="z-index: 2" align="center" justify="center" class="mt-4">
      <v-col cols="10" class="text-center">
        <v-autocomplete
          v-model="literalMapData.id"
          :items="literaryMaps"
          item-text="1"
          item-value="0"
          @change="onMapChange"
          return-object
          style="z-index: 1"
        />
      </v-col>
    </v-row>
    <v-row style="z-index: 2" align="center" justify="center">
      <v-col cols="8">
        <v-card>
          <l-map
            ref="myMap"
            @ready="onReady()"
            v-if="showMap"
            :options="mapOptions"
            style="height: 66vh; width: 100%"
            @update:center="centerUpdate"
          >
            <l-tile-layer
              crossOrigin="true"
              :url="url"
              :attribution="attribution"
            />
            <v-marker-cluster
              ref="clusterRef"
              @ready="onClusterReady()"
              :options="{
                singleMarkerMode: true,
                spiderfyOnMaxZoom: false,
                zoomToBoundsOnClick: false,
                chunkedLoading: true // test this
              }"
            >
              <l-marker
                v-for="mapMarker of mapMarkers"
                v-bind:key="mapMarker.id"
                :lat-lng="mapMarker.coords"
              >
                <l-popup
                  :content="JSON.stringify(mapMarker, null, '\n')"
                ></l-popup>
              </l-marker>
            </v-marker-cluster>
          </l-map>
        </v-card>
      </v-col>
      <v-col cols="3" class="text-center">
        <v-row justify="center" align="center">
          <v-col class="text-center">
            <v-checkbox
              label="Turbo!"
              :disabled="timelineSwitch || offlineMode"
              @change="getDataFromServer"
              v-model="turbo"
            />
          </v-col>
        </v-row>
        <v-row justify="center" align="center">
          <v-col class="text-center">
            <v-textarea
              v-if="!timelineSwitch"
              outlined
              label="Lokacje z okna czasowego"
              :value="visibleMarkers"
              readonly
            ></v-textarea>
          </v-col>
        </v-row>
        <v-row justify="center" align="center">
          <v-col class="text-center">
            <v-textarea
              label="Lokacje z wybranego punktu"
              :value="clickedMarkers"
              readonly
              filled
            ></v-textarea>
          </v-col>
        </v-row>
      </v-col>
    </v-row>
    <v-row align="center" justify="center">
      <v-col cols="10" class="text-center">
        <v-card v-if="timelineSwitch">
          <v-card-text>
            <v-btn
              @click="changeLocationBtn('prev')"
              :disabled="!timelineSwitch || timelineSliderValue === 0"
              >Poprzednia lokacja
            </v-btn>
            <v-btn
              @click="changeLocationBtn('next')"
              :disabled="
                !timelineSwitch || timelineSliderValue === timelineSliderMax
              "
            >
              Następna lokacja
            </v-btn>
            <v-slider
              :max="timelineSliderMax"
              :disabled="!timelineSwitch"
              v-model="timelineSliderValue"
              step="1"
              thumb-label
              ticks
              :label="currentLocation"
            >
            </v-slider>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
    <v-row align="center" justify="center">
      <v-col cols="10" class="text-center">
        <v-card v-if="!timelineSwitch">
          <v-row align="center" justify="center">
            <v-col>
              <v-card-text>Szerokość okna</v-card-text>
            </v-col>
            <v-col cols="10" class="text-left">
              <vue-slider
                class="mr-3"
                v-model="windowWidthSlider"
                :contained="true"
                :marks="marks"
                :min="1"
                :max="100"
                :lazy="!fastPreviewCheck"
              ></vue-slider>
            </v-col>
          </v-row>
          <v-row align="center" justify="center">
            <v-col>
              <v-card-text>Zakres lokacji</v-card-text>
            </v-col>
            <v-col cols="10" class="text-left">
              <vue-slider
                class="mr-3"
                v-model="windowSlider"
                tooltip="none"
                :process="process"
                :fixed="true"
                :contained="true"
                :marks="marksFromLocations"
                :hide-label="true"
                :min="0"
                :max="100"
                :lazy="!fastPreviewCheck"
              >
                <template v-slot:process="{ style }">
                  <div class="vue-slider-process" :style="style">
                    <div
                      :class="[
                        'merge-tooltip',
                        'vue-slider-dot-tooltip-inner',
                        'vue-slider-dot-tooltip-inner-top'
                      ]"
                    >
                      {{ windowSlider[0] }} - {{ windowSlider[1] }}%
                    </div>
                  </div>
                </template>
              </vue-slider>
            </v-col>
          </v-row>
          <v-row justify="center" align="center">
            <v-col cols="2" class="text-center">
              <v-checkbox
                v-model="fastPreviewCheck"
                :label="'Aktualizacja na żywo'"
              ></v-checkbox>
            </v-col>
          </v-row>
        </v-card>
      </v-col>
    </v-row>
    <v-row justify="center" align="center">
      <v-col cols="auto" class="text-center">
        <v-btn @click="timelineSwitch = !timelineSwitch" color="primary">
          {{ timelineSwitch ? "okno" : "po kolei" }}
        </v-btn>
      </v-col>
    </v-row>
    <v-row justify="center" align="center">
      <v-col cols="auto" class="text-center">
        <v-file-input label="Wybierz plik..." v-model="fileToUpload" />
        <v-btn @click="onLoad()" small color="primary">
          Wczytaj dane z pliku
        </v-btn>
      </v-col>
      <v-col cols="auto" class="text-center">
        <v-btn @click="onSave()" small color="primary">
          Zapisz dane do pliku
        </v-btn>
      </v-col>
    </v-row>
    <v-dialog v-model="isFileToUpload" max-width="300">
      <v-card color="warning">
        <v-card-title>Nie wybrałeś pliku!</v-card-title>

        <v-card-text>
          Aby załadować dane wybierz plik.
        </v-card-text>

        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn text @click="isFileToUpload = false">
            OK
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script>
import L from "leaflet";
import "leaflet/dist/leaflet.css";

import { LMap, LTileLayer, LMarker, LPopup } from "vue2-leaflet";
import Vue2LeafletMarkerCluster from "vue2-leaflet-markercluster";
import "leaflet-easyprint";
import axios from "axios";
import { saveAs } from "file-saver";
import VueSlider from "vue-slider-component";
import "vue-slider-component/theme/default.css";

export default {
  name: "VisualiseLocations",
  components: {
    LMap,
    LTileLayer,
    LMarker,
    LPopup,
    "v-marker-cluster": Vue2LeafletMarkerCluster,
    VueSlider
  },
  data() {
    return {
      center: L.latLng(47.41322, -1.219482),
      url: "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
      crossOrigin: null,
      attribution:
        '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors',
      mapOptions: {
        zoomSnap: 1
      },
      mapSelectModel: 0,
      literalMapData: {},
      literaryMaps: [],
      showMap: true,
      locations: null,
      mapMarkers: null,
      map: null,
      id: 0,
      timelineSwitch: false,
      timelineSliderValue: 0,
      timelineSliderMax: 10,
      currentLocation: "Location",
      fileToUpload: null,
      isFileToUpload: null,
      windowSlider: [0, 100],
      windowWidthSlider: 100,
      process: windowSlider => [[windowSlider[0], windowSlider[1]]],
      marks: [1, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
      marksFromLocations: null,
      locationsSliderType: "window",
      visibleMarkers: "",
      fastPreviewCheck: true,
      clickedMarkers: "",
      turbo: true,
      offlineMode: false
    };
  },
  watch: {
    "$attrs.id": function() {
      this.id = this.$attrs.id;
      this.timelineSwitch = false;
      this.getDataFromServer();
    },
    timelineSwitch: function() {
      this.timelineOnOff();
    },
    timelineSliderValue: function() {
      this.updatemapMarkersTimeline();
    },
    windowWidthSlider: function() {
      this.updateSliderWindowWidth();
    },
    windowSlider: function() {
      this.updatemapMarkersWindow();
    }
  },
  methods: {
    onReady() {
      // Map object is not immediately available therefore:
      this.map = this.$refs.myMap.mapObject;
      this.map.setZoom(2);
      L.easyPrint({
        title: "My awesome print button",
        position: "bottomleft",
        sizeModes: ["Current", "A4Portrait", "A4Landscape"],
        exportOnly: true,
        filename: "WWZD Map"
      }).addTo(this.map);
    },
    onClusterReady() {
      this.$refs.clusterRef.mapObject.on("clusterclick", a => {
        this.clickedMarkers = a.layer
          .getAllChildMarkers()
          .sort((a, b) => {
            const el1 = JSON.parse(a._popup._content).time;
            const el2 = JSON.parse(b._popup._content).time;
            return el1 - el2;
          })
          .reduce((s, marker) => {
            const element = JSON.parse(marker._popup._content);
            return `${s}${element.time.toFixed(1)}% ${element.name} ${
              element.orth ? `(${element.orth})` : ""
            } \n`;
          }, "");
      });
      this.$refs.clusterRef.mapObject.on("click", a => {
        a.sourceTarget.closePopup();
        console.log(a.sourceTarget._popup._content);
        const element = JSON.parse(a.sourceTarget._popup._content);
        this.clickedMarkers = `${element.time.toFixed(1)}% ${element.name} ${
          element.orth ? `(${element.orth})` : ""
        }\n`;
      });
    },
    centerUpdate(center) {
      // For future optimalizations:
      // this.map.getBounds()
      // this.map.getZoom()
      if (!this.timelineSwitch) {
        this.getDataFromServer(true);
      }
    },
    fetchInitData() {
      this.id = this.$attrs.id;
      this.getMapsList();
      if (this.id !== 0) {
        this.getDataFromServer();
      }
    },
    onMapChange(event) {
      this.offlineMode = false;
      this.$router.push({
        name: "VisualiseLocations",
        params: { id: event[0] }
      });
    },
    getMapsList() {
      axios
        .get("http://127.0.0.1:5000/literaryMaps")
        .then(response => {
          this.literaryMaps = response.data.literaryMaps;
          console.log(response.data.literaryMaps);
        })
        .catch(e => {
          this.errors.push(e);
        });
    },

    getDataFromServer(fromCoordsUpdate = false) {
      if ((fromCoordsUpdate && this.turbo) || this.offlineMode) return;
      let queryParams = {};
      if (this.turbo) {
        queryParams = {
          id: this.id
        };
      } else {
        queryParams = {
          id: this.id,
          x1: this.map.getBounds().getNorthWest().lng,
          y1: this.map.getBounds().getNorthWest().lat,
          x2: this.map.getBounds().getSouthEast().lng,
          y2: this.map.getBounds().getSouthEast().lat
        };
      }

      axios
        .get("http://127.0.0.1:5000/processText", { params: queryParams })
        .then(response => {
          this.literalMapData = response.data;
          if (this.literalMapData.status !== "ready") {
            this.$router.push({ name: "MapsList" });
          }
          this.locations = [...this.literalMapData.nodesData];
          this.mapMarkers = [...this.literalMapData.nodesData];
          this.marksFromLocations = this.literalMapData.nodesData.map(node => {
            return node.time;
          });
          if (!fromCoordsUpdate) this.timelineOnOff();
        })
        .catch(err => {
          if (err.response.status === 404) {
            this.$router.push({ name: "MapsList" });
          }
        });
    },
    onSave() {
      const blob = new Blob([JSON.stringify(this.locations)], {
        type: "application/json;charset=utf-8"
      });
      saveAs(blob, "mapData.json");
    },
    onLoad() {
      if (this.fileToUpload) {
        const reader = new FileReader();
        reader.addEventListener("load", event => {
          const tmpData = JSON.parse(event.target.result.toString());
          this.marksFromLocations = tmpData.map(node => {
            return node.time;
          });
          this.locations = tmpData;
          this.fileToUpload = null;
          this.offlineMode = true;
          this.timelineOnOff();
        });
        reader.readAsText(this.fileToUpload, "utf-8");
      } else {
        this.isFileToUpload = true;
      }
    },
    timelineOnOff() {
      this.clickedMarkers = "";
      this.visibleMarkers = "";
      this.timelineSliderValue = 0;
      this.windowSlider = [0, 100];
      this.windowWidthSlider = 100;
      if (this.timelineSwitch) {
        // Timeline on
        this.turbo = true;
        console.log("Timeline on");
        this.timelineSliderMax = this.locations.length - 1;
        this.updatemapMarkersTimeline();
      } else {
        // Timeline off
        console.log("Timeline off");
        this.updatemapMarkersWindow();
      }
    },
    updatemapMarkersTimeline() {
      if (!this.timelineSwitch) return;
      // One marker per tick
      this.mapMarkers = [this.locations[this.timelineSliderValue]];
      this.map.setView(this.mapMarkers[0].coords);
      this.clickedMarkers = `${this.mapMarkers[0].time.toFixed(1)}% ${
        this.mapMarkers[0].name
      } ${this.mapMarkers[0].orth ? `(${this.mapMarkers[0].orth})` : ""}\n`;
      console.log(`Location: ${this.mapMarkers[0].name}`);
      this.currentLocation = this.mapMarkers[0].name;
    },
    updatemapMarkersWindow() {
      if (this.timelineSwitch) return;
      this.mapMarkers = this.locations.filter(location => {
        return (
          location.time >= this.windowSlider[0] &&
          location.time <= this.windowSlider[1]
        );
      });
      this.visibleMarkers = this.mapMarkers
        .sort((a, b) => {
          return a.time - b.time;
        })
        .reduce(
          (s, m) =>
            (s += `${m.time.toFixed(1)}% ${m.name} ${
              m.orth ? `(${m.orth})` : ""
            }\n`),
          ""
        );
    },
    changeLocationBtn(direction) {
      console.log(direction);
      if (direction === "prev") {
        this.timelineSliderValue--;
      } else {
        this.timelineSliderValue++;
      }
    },
    updateSliderWindowWidth() {
      this.windowSlider = [0, this.windowWidthSlider];
    }
  },
  created() {
    this.fetchInitData();
  },
  mounted() {
    delete L.Icon.Default.prototype._getIconUrl;
    L.Icon.Default.mergeOptions({
      iconRetinaUrl: require("leaflet/dist/images/marker-icon-2x.png"),
      iconUrl: require("leaflet/dist/images/marker-icon.png"),
      shadowUrl: require("leaflet/dist/images/marker-shadow.png")
    });
  }
};
</script>
<style>
@import "~leaflet.markercluster/dist/MarkerCluster.css";
@import "~leaflet.markercluster/dist/MarkerCluster.Default.css";
.merge-tooltip {
  position: absolute;
  left: 50%;
  bottom: 100%;
  transform: translate(-50%, -10px);
}
</style>
