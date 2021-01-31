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
                v-model="value2"
                :contained="true"
                :marks="marks"
                :min="1"
                :max="100"
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
                v-model="value"
                tooltip="none"
                :process="process"
                :fixed="true"
                :contained="true"
                :marks="marksFromLocations"
                :hide-label="true"
                :min="0"
                :max="100"
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
                      {{ value[0] }} - {{ value[1] }}%
                    </div>
                  </div>
                </template>
              </vue-slider>
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
      value: [0, 100],
      value2: 100,
      process: value => [[value[0], value[1]]],
      marks: [1, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
      marksFromLocations: null,
      locationsSliderType: "window"
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
    value2: function() {
      this.updateSliderWindowWidth();
    },
    value: function() {
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
    centerUpdate(center) {
      /*
      For future optimalizations:
      this.map.getBounds()
      this.map.getZoom()
      */
    },
    fetchInitData() {
      this.id = this.$attrs.id;
      this.getMapsList();
      if (this.id !== 0) {
        this.getDataFromServer();
      }
    },
    onMapChange(event) {
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

    getDataFromServer() {
      axios
        .get("http://127.0.0.1:5000/processText", { params: { id: this.id } })
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
        })
        .catch(err => {
          if (err.response.status === 404) {
            this.$router.push({ name: "MapsList" });
          }
        });
    },
    onSave() {
      const dataToSave = {};
      dataToSave.locations = this.locations;
      dataToSave.mapMarkers = this.mapMarkers;
      const blob = new Blob([JSON.stringify(dataToSave)], {
        type: "application/json;charset=utf-8"
      });
      saveAs(blob, "mapData.json");
    },
    onLoad() {
      if (this.fileToUpload) {
        const reader = new FileReader();
        reader.addEventListener("load", event => {
          const tmpData = JSON.parse(event.target.result.toString());
          this.locations = tmpData.locations;
          this.mapMarkers = tmpData.mapMarkers;
          this.fileToUpload = null;
        });
        reader.readAsText(this.fileToUpload, "utf-8");
      } else {
        this.isFileToUpload = true;
      }
    },
    timelineOnOff() {
      this.timelineSliderValue = 0;
      this.value = [0, 100];
      this.value2 = 100;
      if (this.timelineSwitch) {
        // Timeline on
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
      console.log(`Location: ${this.mapMarkers[0].name}`);
      this.currentLocation = this.mapMarkers[0].name;
    },
    updatemapMarkersWindow() {
      if (this.timelineSwitch) return;
      this.mapMarkers = [this.locations[this.timelineSliderValue]];
      this.mapMarkers = this.locations.filter(location => {
        return location.time >= this.value[0] && location.time <= this.value[1];
      });
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
      this.value = [0, this.value2];
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
