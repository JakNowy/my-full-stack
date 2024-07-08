import { defineStore } from 'pinia';
import {api, adventureUrls} from 'boot/axios';
import { ref } from 'vue';

export interface Adventure {
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

export const useAdventuresStore = defineStore('adventures', () => {
  const adventures = ref<Adventure[]>([]);
  const loading = ref<boolean>(false);


  const setAdventures = (data: Adventure[]) => {
    loading.value = false
    adventures.value = data
  }

  const fetchAdventures = async (): Promise<Adventure[]> => {
    loading.value = true;
    let adventures: Adventure[] = []
    try {
      const response = await api.get(adventureUrls.listAll, {
        params: {
          page: 1,
          itemsPerPage: 10,
        },
      });
      adventures = response.data
      // Sort adventures so that those with userAdventureId are at the top
      // adventures.value = response.data.sort((a: Adventure, b: Adventure) => {
      //   if (a.userAdventureId && !b.userAdventureId) return -1;
      //   if (!a.userAdventureId && b.userAdventureId) return 1;
      // });
    } catch (error) {
      console.error('Failed to fetch adventures:', error);
    } finally {
      loading.value = false;
    }
    return adventures
  };

  return {
    adventures,
    loading,
    fetchAdventures,
    setAdventures,
  };
});
