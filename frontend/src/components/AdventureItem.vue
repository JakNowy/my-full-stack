<!-- src/components/LogoutButton.vue -->
<template>
  <q-item class="q-pa-lg">
    <q-item-section>
      <q-item-label>{{ adventure.title }}</q-item-label>
      <q-item-label caption>{{ adventure.description }}</q-item-label>
    </q-item-section>
    <q-item-section side>
      <q-item-label>{{ adventure.price }} USD</q-item-label>
    </q-item-section>
  </q-item>
</template>

<script setup lang="ts">
import {PropType} from 'vue';
import {Adventure} from 'stores/adventures-store';


defineProps({
  adventure: {
    type: Object as PropType<Adventure>,
    required: true,
  },
})

</script>

<style scoped>


</style>
