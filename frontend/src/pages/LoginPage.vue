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

<script setup lang="ts">
import { ref } from 'vue';
import { useUserStore } from 'stores/user-store';

const username = ref('');
const password = ref('');
const userStore = useUserStore();

const handleLogin = () => {
  userStore.login(username.value, password.value);
};
</script>
