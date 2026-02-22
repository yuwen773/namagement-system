import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useCityStore = defineStore('city', () => {
  // State
  const selectedCity = ref(null)
  const selectedCityCode = ref(null)
  const selectedStation = ref(null)
  const selectedStationCode = ref(null)

  // Actions
  function setCity(city, code) {
    selectedCity.value = city
    selectedCityCode.value = code
  }

  function setStation(station, code) {
    selectedStation.value = station
    selectedStationCode.value = code
  }

  function clearSelection() {
    selectedCity.value = null
    selectedCityCode.value = null
    selectedStation.value = null
    selectedStationCode.value = null
  }

  return {
    selectedCity,
    selectedCityCode,
    selectedStation,
    selectedStationCode,
    setCity,
    setStation,
    clearSelection
  }
})
