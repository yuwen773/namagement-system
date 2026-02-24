import { defineStore } from 'pinia'
import { ref } from 'vue'

/**
 * Building store for managing building hierarchy and selection
 */
export const useBuildingStore = defineStore(
  'building',
  () => {
    // State
    const buildingTree = ref([]) // Complete campus-building-floor-room tree
    const currentBuilding = ref(null) // Currently selected building
    const currentFloor = ref(null) // Currently selected floor
    const currentRoom = ref(null) // Currently selected room

    // Actions
    function setBuildingTree(tree) {
      buildingTree.value = tree
    }

    function setCurrentBuilding(building) {
      currentBuilding.value = building
    }

    function setCurrentFloor(floor) {
      currentFloor.value = floor
    }

    function setCurrentRoom(room) {
      currentRoom.value = room
    }

    function clearSelection() {
      currentBuilding.value = null
      currentFloor.value = null
      currentRoom.value = null
    }

    // Getters
    const hasSelection = () =>
      currentBuilding.value || currentFloor.value || currentRoom.value

    return {
      buildingTree,
      currentBuilding,
      currentFloor,
      currentRoom,
      setBuildingTree,
      setCurrentBuilding,
      setCurrentFloor,
      setCurrentRoom,
      clearSelection,
      hasSelection,
    }
  },
  {
    persist: {
      key: 'energy-building-store',
      storage: sessionStorage,
    },
  }
)
