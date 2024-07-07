<template>
  <q-layout>
    <q-page-container style="padding-top: 50px">
    <q-page>
      <q-card
        class="bg-yellow-3 text-brown-7 page-margin-responsive opacity"
      >

        <router-view />

      </q-card>
    </q-page>


    </q-page-container>
  </q-layout>
</template>

<script setup lang="ts">
</script>

<style>
.opacity {
  opacity: 87%;
}
@media only screen and (max-width: 767px) {
  /* Mobiles: */
  body {
    background: url("../assets/background/bg-vertical-810.png") no-repeat center top fixed;
    background-size: cover;
  }
  .page-margin-responsive {
    margin: 0 8%;
  }
  .scroll-fixed-height {
    height: 75vh;
  }
}

@media only screen and (min-width: 768px) {
  /* Desktop: */
  body {
    background: url("../assets/background/bg-horizontal-1920.png") no-repeat center top fixed;
  }
  .page-margin-responsive {
    margin: 0 20%;
  }
  .scroll-fixed-height {
    height: 70vh;
  }
}
</style>
