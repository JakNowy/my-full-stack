<template>
  <q-page>
    <q-btn label="Back" to="/adventures" />

    <q-card class="bg-yellow-3 text-brown-7 page-margin-responsive opacity">
      <q-header class="bg-brown-7 text-yellow-3 text-weight-bold q-pa-md text-center">
        Adventure Missions
      </q-header>

      <div class="bg-cyan q-pa-xl" v-if="loading">Loading missions...</div>
      <div v-else class="q-pt-xl">
        <div v-if="currentMission">
          <q-card-section>
            <div class="text-h6">{{ currentMission.title }}</div>
            <div>{{ currentMission.description }}</div>
          </q-card-section>
          <q-list bordered>
            <ObjectiveItem
              v-for="objective in currentMission.objectives"
              :key="objective.id"
              :objective="objective"
              :userAdventureId="userAdventureId"
              :completedObjectives="userAdventure?.completedObjectives || []"
              @objective-solved="handleObjectiveSolved"
            />
          </q-list>
          <q-card-actions align="around">
            <q-btn :disabled="!hasPreviousMission" label="Previous" @click="previousMission" />
            <q-btn :disabled="!hasNextMission" label="Next" @click="nextMission" />
          </q-card-actions>
        </div>
      </div>
    </q-card>
    <q-dialog v-model="isCompleteDialog">
      <q-card>
        <q-card-section>
          <div class="text-h6">Congratulations!</div>
          <div>You have completed the adventure!</div>
        </q-card-section>
        <q-card-actions align="center">
          <q-btn label="Go to Home" @click="goHome" />
        </q-card-actions>
      </q-card>
    </q-dialog>
  </q-page>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useMissionsStore } from 'stores/missions-store';
import { useAdventuresStore } from 'stores/adventures-store';
import ObjectiveItem from 'components/ObjectiveItem.vue';

interface UserAdventure {
  adventureId: number;
  isComplete: boolean;
  currentMissionStep: number;
  completedObjectives: number[];
  userId: number;
  id: number;
}

const route = useRoute();
const router = useRouter();
const missionsStore = useMissionsStore();
const adventuresStore = useAdventuresStore();

const adventureId = parseInt(route.params.adventureId as string);
const loading = ref(true);
const displayedMissionStep = ref(1);
const isCompleteDialog = ref(false);

onMounted(async () => {
  await missionsStore.fetchMissions(adventureId);
  const userAdventure = adventuresStore.adventures.find(adventure => adventure.id === adventureId);
  if (userAdventure) {
    displayedMissionStep.value = userAdventure.currentMissionStep || 1;
  }
  loading.value = false;
});

const userAdventure = computed(() =>
  adventuresStore.adventures.find(adventure => adventure.id === adventureId)
);

const userAdventureId = computed(() => userAdventure.value?.userAdventureId || 0);

const currentMission = computed(() =>
  missionsStore.missions.find(mission => mission.step === displayedMissionStep.value)
);

const hasPreviousMission = computed(() => displayedMissionStep.value > 1);
const hasNextMission = computed(() =>
  displayedMissionStep.value < (userAdventure.value?.currentMissionStep || 1)
);

const previousMission = () => {
  if (hasPreviousMission.value) {
    displayedMissionStep.value--;
  }
};

const nextMission = () => {
  if (hasNextMission.value) {
    displayedMissionStep.value++;
  }
};

const handleObjectiveSolved = (newUserAdventure: UserAdventure) => {
  const currentAdventure = adventuresStore.adventures.find(adventure => adventure.id === newUserAdventure.adventureId);
  if (currentAdventure) {
    Object.assign(currentAdventure, newUserAdventure);
    if (newUserAdventure.isComplete) {
      isCompleteDialog.value = true;
    }
    if (displayedMissionStep.value < newUserAdventure.currentMissionStep) {
      displayedMissionStep.value = newUserAdventure.currentMissionStep;
    }
  }
};

const goHome = () => {
  router.push('/');
};
</script>

<style scoped>
.q-page {
  position: relative;
}
</style>
