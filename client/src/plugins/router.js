import Vue from "vue";
import Router from "vue-router";
import Home from "../pages/Home";
import LoadFile from "../pages/LoadFile";
import MapsList from "../pages/MapsList";
import VisualiseLocations from "../pages/VisualiseLocations";

Vue.use(Router);

export default new Router({
  mode: "history",
  routes: [
    {
      path: "/",
      name: "Home",
      component: Home
    },
    {
      path: "/visualise-locations/:id",
      name: "VisualiseLocations",
      component: VisualiseLocations,
      props: true
    },
    {
      path: "/load-file",
      name: "LoadFile",
      component: LoadFile
    },
    {
      path: "/maps-list",
      name: "MapsList",
      component: MapsList
    }
  ]
});
