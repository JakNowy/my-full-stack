import { defineStore } from 'pinia';
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import {api, userUrls} from 'boot/axios';
import qs from 'qs';

export const useUserStore = defineStore('user', () => {
  const token = ref<string | null>(localStorage.getItem('token'));
  const user = ref<{
    id: number,
    email: string,
    firstName: string,
    lastName: string
  } | null>(null);
  const router = useRouter();

  const setToken = (newToken: string) => {
    token.value = newToken;
    api.defaults.headers.common['Authorization'] = `bearer ${newToken}`;
    localStorage.setItem('token', newToken);
  };

  const refreshUser = async (existingToken: string) => {
    setToken(existingToken)
    try {
      const response = await api.get(userUrls.userMe);
      user.value = response.data;
    } catch (error) {
      if (error.response && error.response.status === 403) {
        logout();
      }
    }
  };

  const login = async (username: string, password: string) => {
    try {
      const response = await api.post(
        userUrls.login, qs.stringify({ username, password })
      );
      setToken(response.data.token.access_token);
      user.value = response.data.user;
      router.push('/');
    } catch (error) {
      console.error(error);
    }
  };

  const register = async (email: string, password: string, firstName: string, lastName: string) => {
    try {
      const response = await api.post(userUrls.register, { email, password, firstName, lastName });
      setToken(response.data.token.accessToken);
      user.value = response.data.user;
      router.push('/');
    } catch (error) {
      console.error(error);
    }
  };

  const logout = () => {
    token.value = null;
    user.value = null;
    localStorage.removeItem('token');
    delete api.defaults.headers.common['Authorization'];
    router.push('/login');
  };

  return {
    token,
    user,
    login,
    register,
    logout,
    refreshUser,
  };
});
