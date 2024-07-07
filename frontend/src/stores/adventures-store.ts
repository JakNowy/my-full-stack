import { defineStore } from 'pinia';
import { ref } from 'vue';
import {api, adventureUrls} from 'boot/axios';

interface Adventure {
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

  const fetchAdventures = async () => {
    loading.value = true;
    try {
      const response = await api.get(adventureUrls.listAll, {
        params: {
          page: 1,
          itemsPerPage: 10,
        },
      });
      // Sort adventures so that those with userAdventureId are at the top
      adventures.value = response.data.sort((a: Adventure, b: Adventure) => {
        console.log(1)
        console.log(a)
        console.log(b)
        if (a.userAdventureId && !b.userAdventureId) return -1;
        if (!a.userAdventureId && b.userAdventureId) return 1;
        return 0;
      });
    } catch (error) {
      console.error('Failed to fetch adventures:', error);
    } finally {
      loading.value = false;
    }
  };

  return {
    adventures,
    loading,
    fetchAdventures,
  };
});
