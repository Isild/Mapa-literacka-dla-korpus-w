<template>
  <v-navigation-drawer v-model="drawer" app>
    <v-list dense>
      <v-list-item link to="/">
        <v-list-item-content>
          <v-list-item-title class="text-center"
            >Strona Główna</v-list-item-title
          >
        </v-list-item-content>
      </v-list-item>
      <v-list-item link :to="{ name: 'VisualiseLocations', params: { id: 0 } }">
        <v-list-item-content>
          <v-list-item-title class="text-center"
            >Wyświetl mapę</v-list-item-title
          >
        </v-list-item-content>
      </v-list-item>
      <v-list-item link to="/load-file">
        <v-list-item-content>
          <v-list-item-title class="text-center"
            >Załaduj Plik</v-list-item-title
          >
        </v-list-item-content>
      </v-list-item>
      <v-list-item link :to="{ name: 'MapsList' }">
        <v-list-item-content>
          <v-list-item-title class="text-center">Lista Map</v-list-item-title>
        </v-list-item-content>
      </v-list-item>
    </v-list>
  </v-navigation-drawer>
</template>

<script>
export default {
  name: "Menu",
  props: {
    drawer: {
      type: Boolean,
      required: true
    }
  }
};
</script>

<style scoped></style>
