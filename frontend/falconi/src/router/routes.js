
const routes = [
  {
    path: '/',
    component: () => import('layouts/MainLayout.vue'),

    children: [
      { path: '', component: () => import('pages/Index.vue') },
      { path: 'registros', component: () => import('pages/RegistroList.vue') },
      { path: 'archivos', component: () => import('pages/Archivos.vue') },
      { path: 'nuevo-registro', component: () => import('pages/RegistroNew.vue') }
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
