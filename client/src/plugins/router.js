import Vue from "vue";
import Router from "vue-router";
import Home from "../pages/Home";
import LoadFile from "../pages/LoadFile";
import GraphList from "../pages/GraphList";
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
      path: "/graph-list",
      name: "GraphList",
      component: GraphList
    }
  ]
});
