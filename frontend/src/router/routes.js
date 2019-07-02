
const routes = [
  {
    path: '/',
    component: () => import('layouts/MainPageLayout.vue'),
    children: [
      { path: '',
        component: () => import('pages/Index.vue'),
        children: [
          {
            path: '',
            component: () => import('components/TestRequest.vue')
          }
        ]
      }
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
