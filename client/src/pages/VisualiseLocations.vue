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
        <div style="height: 800px; width: 800px">
          <l-map
            ref="myMap"
            @ready="onReady()"
            v-if="showMap"
            :options="mapOptions"
            style="height: 80%"
            @update:center="centerUpdate"
          >
            <l-tile-layer :url="url" :attribution="attribution" />
            <v-marker-cluster>
              <l-marker
                v-for="marker of markers"
                v-bind:key="marker.id"
                :lat-lng="marker.coords"
              >
                <l-popup
                  :content="JSON.stringify(marker, null, '\n')"
                ></l-popup>
              </l-marker>
            </v-marker-cluster>
          </l-map>
        </div>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import { Icon, latLng } from "leaflet";
import "leaflet/dist/leaflet.css";

import { LMap, LTileLayer, LMarker, LPopup } from "vue2-leaflet";
import Vue2LeafletMarkerCluster from "vue2-leaflet-markercluster";
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
      center: latLng(47.41322, -1.219482),
      url: "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
      attribution:
        '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors',
      mapOptions: {
        zoomSnap: 1
      },
      mapSelectModel: 0,
      literalMapData: {},
      literaryMaps: [],
      showMap: true,
      markers: null,
      map: null,
      id: 0,
      inputUrl:
        "https://gist.githubusercontent.com/DawidPiechota/58e754ed0ab6e0e05a27eeb421fd98b1/raw/6878d98e1dc87ccfc93ac45b7b6d9aa6faf0ec8d/locations.json"
    };
  },
  watch: {
    "$attrs.id": function() {
      this.id = this.$attrs.id;
      this.getDataFromServer();
    }
  },
  methods: {
    onReady() {
      // Map object is not immediately available therefore:
      this.map = this.$refs.myMap.mapObject;
      this.map.setZoom(2);
    },
    centerUpdate(center) {
      // console.clear();
      console.group("Map bounds and center. Zoom level");
      console.log(`zoom: ${this.map.getZoom()}`);
      console.table(this.map.getBounds());
      console.table(center);
      console.groupEnd();
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
          this.markers = [...this.literalMapData.nodesData];
        })
        .catch(err => {
          if (err.response.status === 404) {
            this.$router.push({ name: "MapsList" });
          }
        });
    }
  },
  created() {
    this.fetchInitData();
  },
  mounted() {
    delete Icon.Default.prototype._getIconUrl;
    Icon.Default.mergeOptions({
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
