// Format a Date object to YYYY-MM-DD
export function formatDate(dateObj) {
  const yyyy = dateObj.getFullYear();
  const mm = String(dateObj.getMonth() + 1).padStart(2, "0");
  const dd = String(dateObj.getDate()).padStart(2, "0");
  return `${yyyy}-${mm}-${dd}`;
}

// Shift a date string by ±N days and return new formatted string
export function shiftDate(dateStr, direction) {
  const dateObj = new Date(dateStr);
  dateObj.setDate(dateObj.getDate() + direction);
  return formatDate(dateObj);
}
