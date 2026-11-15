import assert from 'node:assert/strict';
import test from 'node:test';
import { getGradeInfo } from '../src/grade-info.js';

test('grade previews match the prototype backend bands and rounding', () => {
  for (const [mark, grade, points] of [
    [0, 'F', 0], [39.4, 'F', 0], [39.5, 'D', 1], [40, 'D', 1],
    [50, 'C-', 1.7], [55, 'C', 2], [60, 'C+', 2.3], [65, 'B-', 2.7],
    [70, 'B', 3], [75, 'B+', 3.3], [80, 'A-', 3.7], [84.5, 'A-', 3.7],
    [85, 'A', 4], [89.5, 'A+', 4], [90, 'A+', 4], [100, 'A+', 4],
  ]) {
    const result = getGradeInfo(mark);
    assert.equal(result.grade, grade, `grade at ${mark}`);
    assert.equal(result.gp, points, `points at ${mark}`);
  }
});
