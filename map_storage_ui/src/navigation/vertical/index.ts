// ** Type import
import { VerticalNavItemsType } from 'src/@core/layouts/types'

const navigation = (): VerticalNavItemsType => {
  return [
    {
      title: 'Map',
      path: '/map',
      icon: 'mdi:map-search-outline',
    },
    {
      title: 'Map Layers',
      path: '/map-layers',
      icon: 'mdi:sitemap',
    },
  ]
}

export default navigation
