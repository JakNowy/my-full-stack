import { route } from 'quasar/wrappers';
import {
  createMemoryHistory,
  createRouter,
  createWebHashHistory,
  createWebHistory, NavigationGuardNext, RouteLocationNormalized,
} from 'vue-router';
import routes from './routes';
import {useUserStore} from 'stores/user-store';

/*
 * If not building with SSR mode, you can
 * directly export the Router instantiation;
 *
 * The function below can be async too; either use
 * async/await or return a Promise which resolves
 * with the Router instance.
 */

export default route(function (/* { store, ssrContext } */) {
  const createHistory = process.env.SERVER
    ? createMemoryHistory
    : (process.env.VUE_ROUTER_MODE === 'history' ? createWebHistory : createWebHashHistory);

  const Router = createRouter({
    scrollBehavior: () => ({ left: 0, top: 0 }),
    routes,

    // Leave this as is and make changes in quasar.conf.js instead!
    // quasar.conf.js -> build -> vueRouterMode
    // quasar.conf.js -> build -> publicPath
    history: createHistory(process.env.VUE_ROUTER_BASE),
  });

  Router.beforeEach(async (
    to: RouteLocationNormalized,
    from: RouteLocationNormalized,
    next: NavigationGuardNext
  ) => {
    const userStore = useUserStore();
    if (!to.meta.requiresAuth) {
      if (to.fullPath === '/') {
        if (!userStore.user && userStore.token) {
          await userStore.refreshUser(userStore.token)
          next()
        } else {
          next()
        }
      } else {
        next()
      }
    } else {
      if (userStore.user)
      {
        next()
      } else {
        if (userStore.token) {
          await userStore.refreshUser(userStore.token)
          if (userStore.user) {
            next()
          } else {
            next('/login')
          }
        } else {
          next('/login')
        }
      }
    }
  })


  //   if (to.meta.requiresAuth) {
  //     if (userStore.token) {
  //       if (!userStore.user) {
  //         await userStore.refreshUser(userStore.token)
  //         if (userStore.user) {
  //           next();
  //         } else {
  //           next('/login');
  //         }
  //       } else {
  //         next()
  //       }
  //     } else {
  //       if (to.fullPath === '/') {
  //         if (userStore.token && !userStore.user) {
  //         await userStore.refreshUser(userStore.token)
  //         if (userStore.user) {
  //           next();
  //         } else {
  //           next('/login');
  //         }
  //       }
  //       else {
  //         next('/login');
  //       }
  //     }
  //   } else {
  //         console.log(7)
  //     next();
  //   }
  // });

  return Router;
});
