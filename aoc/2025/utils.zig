const std = @import("std");

const MAX_INPUT_SIZE = 1024 * 1024;

pub fn read_input(allocator: std.mem.Allocator, year: i32, day: i32) ![]u8 {
    const input_dir = "inputs";
    const cwd = std.fs.cwd();

    _ = cwd.openDir(input_dir, .{}) catch |err| {
        if (err == error.FileNotFound) {
            try cwd.makeDir(input_dir);
        } else return err;
    };

    const filename = try std.fmt.allocPrint(allocator, "{d}.txt", .{day});
    defer allocator.free(filename);

    const file_path = try std.fs.path.join(allocator, &[_][]const u8{ input_dir, filename });
    defer allocator.free(file_path);

    const input_file = cwd.openFile(file_path, .{}) catch |err| {
        if (err != error.FileNotFound) return err;

        const input = try makeRequest(allocator, year, day);

        var new_file = try cwd.createFile(file_path, .{});
        defer new_file.close();
        try new_file.writeAll(input);
    };
    defer input_file.close();

    return try input_file.readToEndAlloc(allocator, MAX_INPUT_SIZE);
}

fn makeRequest(allocator: std.mem.Allocator, year: i32, day: i32) ![]u8 {
    var client = std.http.Client.init(allocator);
    defer client.deinit();

    const url = try std.fmt.allocPrint(
        allocator,
        "https://adventofcode.com/{d}/day/{d}/input",
        .{ year, day },
    );
    defer allocator.free(url);

    const token = try std.process.getEnvVarOwned(allocator, "AOC_TOKEN");
    defer allocator.free(token);

    var header_buf: [1024]u8 = undefined;
    var req = try client.request(.GET, url, &header_buf, .{ .server_header_buffer = &header_buf });
    defer req.deinit();

    try req.headers.append("Cookie", token);
    try req.send();

    return try req.readAllAlloc(allocator, MAX_INPUT_SIZE);
}

pub fn print_result(year: i32, day: i32, half: i32, result: []const u8) void {
    std.debug.print("Result for [{d}-{d}-{d}]: {s}\n", .{ year, day, half, result });
}
