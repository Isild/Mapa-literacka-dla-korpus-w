<template>
  <v-app id="app">
    <Menu v-bind:drawer="drawer" />
    <AppBar v-bind:change-drawer="changeDrawer" />
    <v-content>
      <v-container>
        <router-view />
      </v-container>
    </v-content>
    <Footer />
  </v-app>
</template>

<script>
import Menu from "../components/Layout/Menu";
import AppBar from "../components/Layout/AppBar";
import Footer from "../components/Layout/Footer";

export default {
  props: {
    source: String
  },
  components: {
    Footer,
    AppBar,
    Menu
  },
  data: () => ({
    drawer: false
  }),
  methods: {
    changeDrawer() {
      this.drawer = !this.drawer;
    }
  }
};
</script>
