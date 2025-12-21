import axios from 'axios'

const aladinApi = axios.create({
  baseURL: '/aladin',
})

export default aladinApi
