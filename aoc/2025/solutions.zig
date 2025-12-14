const std = @import("std");
const utils = @import("utils.zig");

pub fn day1() !void {
    var gpa = std.heap.GeneralPurposeAllocator(.{}){};
    defer _ = gpa.deinit();

    const input = utils.readInput(gpa.allocator(), 2025, 1);

    var it = std.mem.splitSequence(u8, input, "\n");
    var dial: i32 = 50;
    var zeros: i32 = 0;

    while (it.next()) |line| {
        var sign: i32 = undefined;
        if (line[0] == 'R') {
            sign = 1;
        } else {
            sign = -1;
        }

        const turn = try std.math.rem(i32, try std.fmt.parseInt(i32, line[1..], 10), 100);
        dial += (sign * turn);
        if (dial >= 100) {
            dial -= 100;
        } else if (dial < 0) {
            dial += 100;
        }

        if (dial == 0) zeros += 1;
    }

    var buf: [32]u8 = undefined;
    const result = std.fmt.bufPrint(&buf, "{d}", .{zeros}) catch unreachable;
    utils.printResult(2025, 1, 1, result);
}
