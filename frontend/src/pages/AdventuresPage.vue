<template>
  <q-page>
    <logout-button />
    <q-btn label="Home" to="/" />
    <q-card
      class="bg-yellow-3 text-brown-7 page-margin-responsive opacity"
    >

      <q-header
        class="bg-brown-7 text-yellow-3 text-weight-bold q-pa-md text-center">
        My Adventures
      </q-header>

      <div class="bg-cyan" v-if="loading">Loading adventures...</div>
      <div v-else>
        <q-list bordered>
          <q-item v-for="adventure in adventures" :key="adventure.id">
            <q-item-section>
              <q-item-label>{{ adventure.title }}</q-item-label>
              <q-item-label caption>{{ adventure.description }}</q-item-label>
            </q-item-section>
            <q-item-section side>
              <q-item-label>{{ adventure.price }} USD</q-item-label>
            </q-item-section>
          </q-item>
        </q-list>
      </div>

    </q-card>
  </q-page>
</template>

<script lang="ts">
import { defineComponent, onMounted } from 'vue';
import { useAdventuresStore } from 'stores/adventures-store';
import LogoutButton from 'components/LogoutButton.vue';

export default defineComponent({
  components: {LogoutButton},
  setup() {
    const adventuresStore = useAdventuresStore();

    onMounted(() => {
      adventuresStore.fetchAdventures();
    });

    return {
      adventures: adventuresStore.adventures,
      loading: adventuresStore.loading,
    };
  },
});
</script>

<style>
/* Mobiles: */
@media only screen and (max-width: 767px) {
}

/* Desktop: */
@media only screen and (min-width: 768px) {
}

.adventure-section {
  border-top: 1px solid sandybrown;
}
</style>
