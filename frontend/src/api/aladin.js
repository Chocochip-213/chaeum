import axios from 'axios'

const aladinApi = axios.create({
  baseURL: '/ttb/api',
  headers: {
    'Content-Type': 'application/json',
  },
})

export default aladinApi
