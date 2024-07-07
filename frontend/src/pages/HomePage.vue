<!-- src/components/Homepage.vue -->
<template>
  <q-page>
    <div v-if="user">
      <h1>Welcome, {{ user.firstName }} {{ user.lastName }}</h1>
      <p>{{ user.email }}</p>
      <q-btn label="Logout" @click="logout" />
    </div>
    <div v-else>
      <q-btn color="primary" label="Login" to="login"/>
      <q-btn color="secondary" label="Register" to="register"/>
    </div>
  </q-page>
</template>

<script lang="ts">
import { defineComponent, onMounted } from 'vue';
import { useUserStore } from 'stores/user-store';

export default defineComponent({
  setup() {
    const userStore = useUserStore();
    const user = userStore.user;

    onMounted(() => {
      userStore.fetchUser();
    });

    const logout = () => {
      userStore.logout();
    };

    return {
      user,
      logout
    };
  }
});
</script>
