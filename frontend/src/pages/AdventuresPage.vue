<template>
  <q-page>
    <logout-button />
    <q-btn label="Home" to="/" />
    <q-card class="bg-yellow-3 text-brown-7 page-margin-responsive opacity">
      <q-header class="bg-brown-7 text-yellow-3 text-weight-bold q-pa-md text-center">
        My Adventures
      </q-header>

      <div class="bg-cyan q-pa-xl" v-if="loading">Loading adventures...</div>
      <div v-else class="q-pt-xl">
        <q-list bordered>
          <AdventureItem v-for="adventure in adventures" :key="adventure.id"
                         :adventure="adventure"/>
        </q-list>
      </div>
    </q-card>
  </q-page>
</template>

<script lang="ts" setup>
import { onMounted, computed } from 'vue';
import {useAdventuresStore} from 'stores/adventures-store';
import LogoutButton from 'components/LogoutButton.vue';
import AdventureItem from 'components/AdventureItem.vue';
import {AxiosError} from 'axios';

const adventuresStore = useAdventuresStore();
const adventures = computed(() => adventuresStore.adventures);
const loading = computed(() => adventuresStore.loading);

onMounted(() => {
  adventuresStore.fetchAdventures()
    .then((data) => {
      adventuresStore.setAdventures(data)
    })
    .catch((error: AxiosError) => {
      console.error('Error fetching adventures:', error);
    });
});



</script>

<style scoped>
.q-page {
  position: relative;
}
.logout-button {
  position: absolute;
  top: 10px;
  right: 10px;
}
</style>
