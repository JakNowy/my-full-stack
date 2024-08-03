<template>
  <q-list bordered>

    <q-item class="q-pa-lg adventure-item" v-for="adventure in adventures" :key="adventure.id">
      <q-item-section>
  <!--      @click="goToMissions(adventure.id)-->
        <q-item-label class="text-bold">{{ adventure.title }}</q-item-label>
        <q-item-label v-if="adventure.userAdventureId">
          UA: {{ adventure.userAdventureId }}
        </q-item-label>
        <q-item-label caption>{{ adventure.description }}</q-item-label>
      </q-item-section>

      <q-item-section side>
        <q-item-label>{{ adventure.price }} USD</q-item-label>
      </q-item-section>
      <q-btn v-if="adventure.userAdventureId"
             @click="goToMission(adventure.id)">Go to
      </q-btn>
      <q-btn v-else @click="purchaseAdventure(adventure.id)">Purchase</q-btn>
    </q-item>

  </q-list>
</template>

<script setup lang="ts">
import {PropType} from 'vue';
import {Adventure} from 'stores/adventures-store';
import {useRouter} from 'vue-router';


const router = useRouter()

// const status = (adventure) => {
//   // todo: implement status interface and calculate in store
//   if (!adventure.id) {
//     return 'toPurchase'
//   } else {
//     return adventure.isComplete ? 'complete' : 'inProgress'
//   }
// }

defineProps({
  adventures: {
    type: Array as PropType<Adventure[]>,
    required: true,
  },
})

const goToMission = (adventureId: number) => {
  router.push({ path: `/missions/${adventureId}` });
};

const purchaseAdventure = (adventureId: number) => {
  console.log(`Purchasing adventure ${adventureId}`)
}

</script>

<style scoped lang="scss">
  .adventure-item {
    border-bottom: 20px black;
    //background-color: #ffd6d6;
    background-color: $secondary;
    color: $accent;
  }
</style>
