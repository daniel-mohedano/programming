const std = @import("std");
const utils = @import("utils.zig");

pub fn day1() void {
    var gpa = std.heap.GeneralPurposeAllocator(.{}){};
    defer gpa.deinit();

    const input = try utils.read_input(gpa.allocator(), 2025, 1);

    var it = std.mem.splitSequence(u8, input, "\n");
    var dial = 50;
    var zeros = 0;

    while (it.next()) |line| {
        var sign: i32 = undefined;
        if (line[0] == 'R') {
            sign = 1;
        } else {
            sign = -1;
        }

        const turn = std.math.rem(i32, std.fmt.parseInt(i32, line[1..], 10), 100);
        dial += (sign * turn);
        if (dial >= 100) {
            dial -= 100;
        } else if (dial < 0) {
            dial += 100;
        }

        if (dial == 0) zeros += 1;
    }

    utils.print_result(2025, 1, 1, zeros);
}
