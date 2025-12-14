const std = @import("std");

const MAX_INPUT_SIZE = 232072;

pub fn splitLines(allocator: std.mem.Allocator, buf: []u8) [][]const u8 {
    var lines: std.ArrayList([]const u8) = .{};
    defer lines.deinit(allocator);
    var iter = std.mem.splitAny(u8, buf, "\n");
    while (iter.next()) |line| lines.append(allocator, line) catch unreachable;
    // remove empty last line
    if (lines.items[lines.items.len - 1].len == 0) _ = lines.pop();
    return lines.items;
}

fn readFile(allocator: std.mem.Allocator, filename: []const u8) []u8 {
    var file = std.fs.cwd().openFile(filename, .{}) catch {
        std.debug.panic("file not found: {s}\n", .{filename});
    };
    defer file.close();
    return file.readToEndAlloc(allocator, MAX_INPUT_SIZE) catch {
        std.debug.panic("error reading: {s}\n", .{filename});
    };
}

fn downloadFile(allocator: std.mem.Allocator, url: []u8, path: []u8, cookie: ?[]const u8) !void {
    std.debug.print("downloading {s} from {s}\n", .{ path, url });
    var client = std.http.Client{ .allocator = allocator };
    defer client.deinit();

    const uri = try std.Uri.parse(url);
    var req = try client.request(.GET, uri, .{
        .extra_headers = &[_]std.http.Header{.{ .name = "Cookie", .value = cookie orelse "" }},
    });
    defer req.deinit();

    try req.sendBodiless();

    var response_obj = try req.receiveHead(&.{});

    if (response_obj.head.status != .ok) {
        return error.FailedToFetchInputFile;
    }

    var response: std.ArrayList(u8) = .{};
    defer response.deinit(allocator);

    var reader = response_obj.reader(&.{});
    try reader.appendRemaining(allocator, &response, std.Io.Limit.limited(MAX_INPUT_SIZE));

    const dir = try std.fs.cwd().makeOpenPath(std.fs.path.dirname(path).?, .{});
    const file = try dir.createFile(std.fs.path.basename(path), .{});
    defer file.close();
    try file.writeAll(response.items);
}

pub fn readInput(allocator: std.mem.Allocator, year: i32, day: i32) []u8 {
    const filename = std.fmt.allocPrint(allocator, "input/day{d}.txt", .{day}) catch unreachable;
    std.fs.cwd().access(filename, .{}) catch |err| {
        if (err == error.FileNotFound) {
            const cookie = std.process.getEnvVarOwned(allocator, "AOC_TOKEN") catch "";
            const url = std.fmt.allocPrint(
                allocator,
                "https://adventofcode.com/{d}/day/{d}/input",
                .{ year, day },
            ) catch unreachable;
            downloadFile(allocator, url, filename, cookie) catch {};
        }
    };

    const buf = readFile(allocator, filename);
    return buf;
}

pub fn printResult(year: i32, day: i32, half: i32, result: []const u8) void {
    std.debug.print("Result for [{d}-{d}-{d}]: {s}\n", .{ year, day, half, result });
}
