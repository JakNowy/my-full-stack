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

<script lang="ts">
import {defineComponent, PropType} from 'vue';
import {Adventure} from 'stores/adventures-store';


export default defineComponent({
  props: {
    adventure: {
      type: Object as PropType<Adventure>,
      required: true,
    },
  },
  setup() {

    return {
    };
  },
});
</script>

<style scoped>


</style>
