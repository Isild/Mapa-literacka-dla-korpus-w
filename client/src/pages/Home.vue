<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <p>
          Zadaniem stworzonej aplikacji jest analiza tekstów literackich, która
          polega na wykrywaniu lokalizacji, wyznaczeniu ich częstości
          występowania oraz kolejności poszczególnych wystąpień. Aplikacja
          wykorzystuje narzędzie NER oraz Polem udostępniane przez
          <a target="_blank" :href="'//' + 'www.clarin-pl.eu'"
            >www.clarin-pl.eu</a
          >.
        </p>
        <p>
          Aplikacja prezentuje wyniki analizy w postaci mapy z zaznaczonymi
          punktami. Jej funkcje umożliwiają wyświetlanie informacji o wszystkich
          znalezionych miejscach w tekście, które są prezentowane jako
          lokalizacją oznaczone na mapie.
        </p>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="1"></v-col>
      <v-col cols="4">
        <v-img src="@/assets/images/upload-tekstu.png"></v-img>
      </v-col>
      <v-col cols="1"></v-col>
      <v-col cols="6">
        <p>
          Wczytywanie tekstu możliwe jest po wpisaniu go ręcznie lub poprzez
          wczytanie pliku.
        </p>
        <p>
          Program obsługuje pliki tekstowe w następujących formatach: *.txt,
          *.pdf.
        </p>
        <p>
          Plik *.pdf musi zawierać tekst, czytanie tekstu z obrazów (OCR) nie
          jest wspierane.
        </p>
        <p>Po załadowaniu tekstu możliwa jest jego edycja.</p>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="6">
        <p>
          Dane zwracane z przeanalizowanego tekstu zwracają punkty wytąpień
          lokalizacji w tekscie.
        </p>
        <p>
          Poprzez funkcje okna oraz wyświetlania punktów w porządku
          chronologicznym jest możliwa głębsza analiza tekstów.
        </p>
        <p>
          Analizowany tekst zapisywany jest w aplikacji aby umożliwić ponowne
          jego analizę. Dodatkowo możliwe jest pobranie oraz
          wczytanieprzeanalizowanego tekstu.
        </p>
        <p>
          Możliwe jest zapisywanie obecnego widoku mapy do pliku PNG.
        </p>
      </v-col>
      <v-col cols="1"></v-col>
      <v-col cols="4">
        <v-img src="@/assets/images/map.png"></v-img>
      </v-col>
      <v-col cols="1"></v-col>
    </v-row>
    <v-row align="center" justify="center">
      <v-col class="text-center" cols="auto">
        <h1 style="color: #006bad ">Powered By Clarin</h1>
        <v-img src="@/assets/images/clarin.png"></v-img>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
export default {};
</script>

<style scoped>
img {
  width: 100%;
  height: 50%;
}
</style>
