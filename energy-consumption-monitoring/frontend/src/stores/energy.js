import { defineStore } from 'pinia'
import { ref } from 'vue'

/**
 * Energy store for managing energy data query parameters
 */
export const useEnergyStore = defineStore(
  'energy',
  () => {
    // State
    const selectedDevices = ref([]) // Selected device IDs for comparison
    const dateRange = ref([]) // Date range for queries [start, end]
    const energyType = ref('') // Selected energy type (WATER/ELECTRICITY/GAS)
    const periodType = ref('DAY') // Period type for statistics (DAY/MONTH/YEAR)

    // Actions
    function setSelectedDevices(devices) {
      selectedDevices.value = devices
    }

    function addDevice(device) {
      if (!selectedDevices.value.find((d) => d.id === device.id)) {
        selectedDevices.value.push(device)
      }
    }

    function removeDevice(deviceId) {
      selectedDevices.value = selectedDevices.value.filter(
        (d) => d.id !== deviceId
      )
    }

    function clearDevices() {
      selectedDevices.value = []
    }

    function setDateRange(range) {
      dateRange.value = range
    }

    function setEnergyType(type) {
      energyType.value = type
    }

    function setPeriodType(type) {
      periodType.value = type
    }

    // Getters
    const hasFilters = () =>
      selectedDevices.value.length > 0 ||
      dateRange.value.length > 0 ||
      energyType.value !== ''

    return {
      selectedDevices,
      dateRange,
      energyType,
      periodType,
      setSelectedDevices,
      addDevice,
      removeDevice,
      clearDevices,
      setDateRange,
      setEnergyType,
      setPeriodType,
      hasFilters,
    }
  },
  {
    persist: {
      key: 'energy-store',
      storage: sessionStorage,
    },
  }
)
