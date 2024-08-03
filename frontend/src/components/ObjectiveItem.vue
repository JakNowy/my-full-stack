<template>
  <q-item class="q-pa-lg">
    <q-item-section>
      <q-item-label>{{ objective.title }}</q-item-label>
      <q-item-label caption>{{ objective.description }}</q-item-label>
    </q-item-section>
    <q-item-section side>
      <q-icon v-if="isCompleted" name="check_circle" color="green" />
      <q-btn v-else label="Solve" @click="showModal = true" />
    </q-item-section>

    <q-dialog v-model="showModal">
      <q-card>
        <q-card-section>
          <div class="text-h6">{{ objective.title }}</div>
          <div>{{ objective.description }}</div>
          <q-input v-model="solution" label="Solution" debounce="2000" />
        </q-card-section>
        <q-card-actions align="center">
          <q-btn label="Submit" @click="submitSolution" />
          <q-btn label="Cancel" @click="showModal = false" />
        </q-card-actions>
      </q-card>
    </q-dialog>
  </q-item>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';
import { useQuasar } from 'quasar';
import { api } from 'boot/axios';

interface Objective {
  id: number;
  title: string;
  description: string;
}

const props = defineProps({
  objective: {
    type: Object as () => Objective,
    required: true
  },
  userAdventureId: {
    type: Number,
    required: true
  },
  completedObjectives: {
    type: Array as () => number[],
    required: true
  }
});

const emit = defineEmits(['objective-solved']);

const $q = useQuasar();

const showModal = ref(false);
const solution = ref('');

const isCompleted = computed(() =>
  props.completedObjectives.includes(props.objective.id)
);

const submitSolution = async () => {
  try {
    const response = await api.post('http://localhost/api/user_adventures/solve_objective', {
      userAdventureId: props.userAdventureId,
      objectiveId: props.objective.id,
      solution: solution.value
    });
    $q.notify({ type: 'positive', message: 'Solution is correct!' });
    emit('objective-solved', response.data);
    showModal.value = false;
  } catch (error) {
    $q.notify({ type: 'negative', message: 'Solution is incorrect.' });
  }
};
</script>

<style scoped>
.q-item-section {
  display: flex;
  align-items: center;
}
</style>
