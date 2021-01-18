<template>
  <v-container fill-height fluid>
    <v-row style="z-index: 2" align="center" justify="center" class="mt-4">
      <v-col cols="10 " class="text-center">
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
    <v-row style="z-index: 1" align="center" justify="center">
      <v-col cols="10">
        <div style="height: 600px; width: 800px">
          <l-map
            ref="myMap"
            @ready="onReady()"
            v-if="showMap"
            :options="mapOptions"
            style="height: 100%;"
            @update:center="centerUpdate"
          >
            <l-tile-layer
              crossOrigin="true"
              :url="url"
              :attribution="attribution"
            />
            <v-marker-cluster>
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
        </div>
      </v-col>
    </v-row>
    <v-row align="center" justify="center">
      <v-col cols="10" class="text-center">
        <v-card>
          <v-card-text>
            <v-switch
              v-model="timelineSwitch"
              :label="`Oś czasu ${timelineSwitch ? 'włączona' : 'wyłączona'}`"
            ></v-switch>
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
  </v-container>
</template>

<script>
import L from "leaflet";
import "leaflet/dist/leaflet.css";

import { LMap, LTileLayer, LMarker, LPopup } from "vue2-leaflet";
import Vue2LeafletMarkerCluster from "vue2-leaflet-markercluster";
import "leaflet-easyprint";
import axios from "axios";

export default {
  name: "VisualiseLocations",
  components: {
    LMap,
    LTileLayer,
    LMarker,
    LPopup,
    "v-marker-cluster": Vue2LeafletMarkerCluster
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
      currentLocation: "Location"
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
      this.updatemapMarkers();
    }
  },
  methods: {
    onReady() {
      // Map object is not immediately available therefore:
      this.map = this.$refs.myMap.mapObject;
      this.map.setZoom(2);
      L.easyPrint({
        title: "My awesome print button",
        position: "topleft",
        sizeModes: ["Current", "A4Portrait", "A4Landscape"],
        exportOnly: true
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
        })
        .catch(err => {
          if (err.response.status === 404) {
            this.$router.push({ name: "MapsList" });
          }
        });
    },
    timelineOnOff() {
      this.timelineSliderValue = 0;
      if (this.timelineSwitch) {
        // Timeline on
        console.log("Timeline on");
        this.timelineSliderMax = this.locations.length - 1;
        this.updatemapMarkers();
      } else {
        // Timeline off
        console.log("Timeline off");
        this.mapMarkers = [...this.locations];
        this.currentLocation = "Location";
      }
    },
    updatemapMarkers() {
      if (!this.timelineSwitch) return;
      // One marker per tick
      this.mapMarkers = [this.locations[this.timelineSliderValue]];
      this.map.setView(this.mapMarkers[0].coords);
      console.log(`Location: ${this.mapMarkers[0].name}`);
      this.currentLocation = this.mapMarkers[0].name;
    },
    changeLocationBtn(direction) {
      console.log(direction);
      if (direction === "prev") {
        this.timelineSliderValue--;
      } else {
        this.timelineSliderValue++;
      }
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
</style>
