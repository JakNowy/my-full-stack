<!-- src/components/Register.vue -->
<template>
  <q-page>
    <q-card>
      <q-card-section>
        <div class="text-h6">Register</div>
      </q-card-section>
      <q-card-section>
        <q-input v-model="email" label="Email" />
        <q-input v-model="firstName" label="Full Name" />
        <q-input v-model="lastName" label="Full Name" />
        <q-input v-model="password" label="Password" type="password" />
      </q-card-section>
      <q-card-actions align="center">
        <q-btn label="Register" @click="handleRegister" />
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
    const email = ref('');
    const firstName = ref('');
    const lastName = ref('');
    const password = ref('');
    const userStore = useUserStore();

    const handleRegister = () => {
      userStore.register(email.value, password.value, firstName.value, lastName.value);
    };

    return {
      email,
      firstName,
      lastName,
      password,
      handleRegister
    };
  }
});
</script>
