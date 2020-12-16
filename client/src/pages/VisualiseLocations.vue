<template>
  <v-container fill-height fluid>
    <v-row align="center" justify="center">
      <v-col cols="10 " class="text-center">
        <v-text-field
          v-model="inputUrl"
          label="Link do testowania"
        ></v-text-field>
        <v-btn @click="showLongText">
          Get data
        </v-btn>
        <v-btn @click="showMap = !showMap">
          Toggle map
        </v-btn>
      </v-col>
    </v-row>
    <v-row align="center" justify="center">
      <v-col cols="10">
        <div style="height: 800px; width 800px">
          <l-map
            ref="myMap"
            @ready="onReady()"
            v-if="showMap"
            :zoom="zoom"
            :center="center"
            :options="mapOptions"
            style="height: 80%"
            @update:center="centerUpdate"
            @update:zoom="zoomUpdate"
          >
            <l-tile-layer :url="url" :attribution="attribution" />
            <v-marker-cluster>
              <l-marker
                v-for="marker in markers"
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
  name: "Example",
  components: {
    LMap,
    LTileLayer,
    LMarker,
    LPopup,
    "v-marker-cluster": Vue2LeafletMarkerCluster
  },
  data() {
    return {
      zoom: 2,
      center: latLng(47.41322, -1.219482),
      url: "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
      attribution:
        '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors',
      currentZoom: 11.5,
      currentCenter: latLng(47.41322, -1.219482),
      showParagraph: false,
      mapOptions: {
        zoomSnap: 0.5
      },
      showMap: true,
      markers: null,
      map: null,
      inputUrl:
        "https://gist.githubusercontent.com/DawidPiechota/58e754ed0ab6e0e05a27eeb421fd98b1/raw/6878d98e1dc87ccfc93ac45b7b6d9aa6faf0ec8d/locations.json"
    };
  },
  methods: {
    onReady() {
      // Map object is not immediately available therefore:
      this.map = this.$refs.myMap.mapObject;
    },
    zoomUpdate(zoom) {
      // this.currentZoom = zoom * 2;
      this.map.setZoom(zoom);
    },
    centerUpdate(center) {
      this.currentCenter = center;
    },

    /*
      Coords generator:
      [
        '{{repeat(5000)}}',
        {lat: '{{integer(-90, 90)}}', lng: '{{integer(-180, 180)}}'}
      ]
    */
    showLongText() {
      // this.showParagraph = !this.showParagraph;
      axios.get(this.inputUrl).then(response => (this.markers = response.data));
    },
    innerClick() {
      alert("Click!");
    }
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
