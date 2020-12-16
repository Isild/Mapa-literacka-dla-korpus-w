<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <p>
          Zadaniem stworzonej aplikacji jest analiza tekstów literackich, która
          polega na wykryciu bytów, wyznaczeniu ich częstości występowania oraz
          powiązań pomiędzy nimi. Aplikacja umożliwia wgranie tekstu, którego
          wyniki analizy zostają zaprezentowane w postaci grafu.
          Zaimplementowane funkcje umożliwiają przeglądanie oraz edycję
          prezentowanego grafu. Użytkownik posiada możliwość zapisu do pliku
          edytowanego grafu. Dodatkowo aplikacja przechowuje w bazie danych
          wcześniej przeanalizowane grafy, aby użytkownik nie musiał zlecać
          zadania analizy tego samego tekstu dwa razy.
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
          Dane zwracane z przeanalizowanego tekstu zwracają wagi połączeń
          pomiędzy bytami oraz liczbę wystąpień postaci.
        </p>
        <p>
          Użytkownik posiada możliwość ręcznego złączenia dwóch bytów w jeden.
          Przed złączeniem, wybrane byty zostają podświetlone.
        </p>
        <p>
          Funkcjonalność ta jest przydatna w przypadku gdy jeden byt zostanie
          błędnie rozróżniony jako dwa osobne.
        </p>
        <p>
          Wszelkie zmiany dokonane przez użytkownika mogą zostać przywrócone
          przyciskiem Przywróć zmiany.
        </p>
      </v-col>
      <v-col cols="1"></v-col>
      <v-col cols="4">
        <v-img src="@/assets/images/merge.png"></v-img>
      </v-col>
      <v-col cols="1"></v-col>
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
