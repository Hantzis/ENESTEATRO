
const routes = [
  {
    path: '/',
    component: () => import('layouts/MainLayout.vue'),

    children: [
      { path: '', component: () => import('pages/Index.vue') },
      { path: 'registros', component: () => import('pages/Registros.vue') },
      { path: 'archivos', component: () => import('pages/Archivos.vue') },
      { path: 'fondos', component: () => import('pages/Fondos.vue') },
      { path: 'lugares', component: () => import('pages/Lugares.vue') },
      { path: 'ramos', component: () => import('pages/Ramos.vue') },
    ]
  }
]

// Always leave this as last one
if (process.env.MODE !== 'ssr') {
  routes.push({
    path: '*',
    component: () => import('pages/Error404.vue')
  })
}

export default routes
