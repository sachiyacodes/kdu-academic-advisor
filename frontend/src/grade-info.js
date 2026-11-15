export function getGradeInfo(mark) {
  const value = parseFloat(mark) || 0;
  const lower = Math.floor(value);
  const n = value - lower === 0.5 ? lower + (lower % 2) : Math.round(value);
  if (n >= 90) return { grade: 'A+', gp: 4.0, variant: 'success' };
  if (n >= 85) return { grade: 'A',  gp: 4.0, variant: 'success' };
  if (n >= 80) return { grade: 'A-', gp: 3.7, variant: 'success' };
  if (n >= 75) return { grade: 'B+', gp: 3.3, variant: 'primary' };
  if (n >= 70) return { grade: 'B',  gp: 3.0, variant: 'primary' };
  if (n >= 65) return { grade: 'B-', gp: 2.7, variant: 'primary' };
  if (n >= 60) return { grade: 'C+', gp: 2.3, variant: 'warning' };
  if (n >= 55) return { grade: 'C',  gp: 2.0, variant: 'warning' };
  if (n >= 50) return { grade: 'C-', gp: 1.7, variant: 'warning' };
  if (n >= 40) return { grade: 'D',  gp: 1.0, variant: 'warning' };
  return        { grade: 'F',  gp: 0.0, variant: 'danger' };
}
