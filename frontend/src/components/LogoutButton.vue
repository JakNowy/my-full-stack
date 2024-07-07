<!-- src/components/LogoutButton.vue -->
<template>
  <q-btn flat @click="handleLogout" class="logout-button">
    Logout
  </q-btn>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import { useUserStore } from 'stores/user-store';

export default defineComponent({
  setup() {
    const userStore = useUserStore();

    const handleLogout = () => {
      userStore.logout();
    };

    return {
      handleLogout,
    };
  },
});
</script>

<style scoped>
.logout-button {
  position: absolute;
  top: 10px;
  right: 10px;
}
</style>
