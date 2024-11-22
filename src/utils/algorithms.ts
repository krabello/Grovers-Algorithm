export const linearSearch = (size: number): number => {
  // Classical search takes O(n) steps
  return size;
};

export const groverSearch = (size: number): number => {
  // Quantum search takes O(√n) steps
  return Math.ceil(Math.PI / 4 * Math.sqrt(size));
};