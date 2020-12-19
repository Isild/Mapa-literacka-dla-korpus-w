<template>
  <v-app-bar app color="indigo" dark>
    <v-app-bar-nav-icon @click.stop="changeDrawer"></v-app-bar-nav-icon>
    <v-toolbar-title>
      <router-link to="/" class="toolbar-title" exact>
        Mapa literacka
      </router-link>
    </v-toolbar-title>
  </v-app-bar>
</template>

<script>
export default {
  name: "AppBar",
  props: {
    changeDrawer: {
      type: Function,
      required: true
    }
  }
};
</script>

<style scoped>
.toolbar-title {
  text-decoration: none;
  color: #ffffff;
}
</style>
