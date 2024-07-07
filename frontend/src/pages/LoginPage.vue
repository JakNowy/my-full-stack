<!-- src/components/Login.vue -->
<template>
  <q-page>
    <q-card>
      <q-card-section>
        <div class="text-h6">Login</div>
      </q-card-section>
      <q-card-section>
        <q-input v-model="username" label="Email" />
        <q-input v-model="password" label="Password" type="password" />
      </q-card-section>
      <q-card-actions align="center">
        <q-btn label="Login" @click="handleLogin" />
        <q-btn label="Back" to="/" />
      </q-card-actions>
    </q-card>
  </q-page>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue';
import { useUserStore } from 'stores/user-store';

export default defineComponent({
  setup() {
    const username = ref('');
    const password = ref('');
    const userStore = useUserStore();

    const handleLogin = () => {
      userStore.login(username.value, password.value);
    };

    return {
      username,
      password,
      handleLogin
    };
  }
});
</script>
