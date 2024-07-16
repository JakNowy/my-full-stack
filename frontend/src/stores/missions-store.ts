import { defineStore } from 'pinia';
import { ref } from 'vue';
import { api } from 'boot/axios';

export interface Objective {
  description: string;
  solution: string;
  missionId: number;
  id: number;
  title: string;
  objectiveType: number;
  createdAt: string;
}

export interface Mission {
  title: string;
  description: string;
  step: number;
  adventureId: number;
  id: number;
  objectives: Objective[];
}

export const useMissionsStore = defineStore('missions', () => {
  const missions = ref<Mission[]>([]);
  const loading = ref(false);

  const fetchMissions = async (adventureId: number) => {
    loading.value = true;
    try {
      const response = await api.get(`/missions/${adventureId}/get_multi`);
      missions.value = response.data;
    } catch (error) {
      console.error('Failed to fetch missions:', error);
    } finally {
      loading.value = false;
    }
  };

  return {
    missions,
    loading,
    fetchMissions,
  };
});
