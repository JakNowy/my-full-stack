import { defineStore } from 'pinia';
import { api, adventureUrls } from 'boot/axios';
import { ref } from 'vue';

export interface AdventureIn {
  title: string;
  description: string;
  price: number;
  id: number;
  userAdventureId: number | null;
  currentMissionStep: number | null;
  completedObjectives: number[] | null;
  isComplete: boolean | null;
  userId: number | null;
}

export interface Adventure extends AdventureIn {
  status: 'complete' | 'inProgress' | 'purchase'
}

export interface UserAdventure {
  adventureId: number;
  isComplete: boolean;
  currentMissionStep: number;
  completedObjectives: number[];
  userId: number;
  id: number;
}

export const useAdventuresStore = defineStore('adventures', () => {
  const adventures = ref<Adventure[]>([]);
  const loading = ref<boolean>(false);
  const userAdventureId = ref<number | null>(null);
  const completedObjectives = ref<number[]>([]);

  const setAdventures = (data: Adventure[]) => {
    loading.value = false;
    adventures.value = data;
  }

  const fetchAdventures = async (): Promise<Adventure[]> => {
    loading.value = true;
    let fetchedAdventures: Adventure[] = [];
    try {
      const response = await api.get(adventureUrls.listAll, {
        params: {
          page: 1,
          itemsPerPage: 10,
        },
      });
      fetchedAdventures = response.data;
      setAdventures(fetchedAdventures);
    } catch (error) {
      console.error('Failed to fetch adventures:', error);
    } finally {
      loading.value = false;
    }
    return fetchedAdventures;
  };

  const setUserAdventure = (newUserAdventure: UserAdventure) => {
    const adventureIndex = adventures.value.findIndex(adventure => adventure.id === newUserAdventure.adventureId);
    if (adventureIndex !== -1) {
      adventures.value[adventureIndex] = { ...adventures.value[adventureIndex], ...newUserAdventure };
      userAdventureId.value = newUserAdventure.id;
      completedObjectives.value = newUserAdventure.completedObjectives || [];
    }
  };

  const updateUserAdventure = (updatedAdventure: Adventure) => {
    const index = adventures.value.findIndex(adventure => adventure.id === updatedAdventure.id);
    if (index !== -1) {
      adventures.value[index] = updatedAdventure;
    }
  };

  const updateAdventure = (updatedAdventure: Adventure) => {
    const index = adventures.value.findIndex(
      adventure => adventure.id === updatedAdventure.id
    );
    if (index !== -1) {
      adventures.value[index] = { ...adventures.value[index], ...updatedAdventure };
    }
  };

  return {
    adventures,
    loading,
    userAdventureId,
    completedObjectives,
    fetchAdventures,
    setAdventures,
    setUserAdventure,
    updateUserAdventure,
    updateAdventure,
  };
});
