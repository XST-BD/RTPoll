-- KEYS:
-- 1: voter_key
-- 2: votes_key
-- 3: fp_key
-- 4: ip_key
-- 5: block_key

-- ARGV:
-- 1: new_option
-- 2: now_ts
-- 3: fp_limit
-- 4: ip_limit
-- 5: cooldown


local voter_key     = KEYS[1]
local votes_key     = KEYS[2]
local fp_key        = KEYS[3]
local ip_key        = KEYS[4]
local block_key     = KEYS[5]

local new_option    = ARGV[1]
local now           = tonumber(ARGV[2])
local fp_limit      = tonumber(ARGV[3])
local ip_limit      = tonumber(ARGV[4])
local cooldown      = tonumber(ARGV[5])


-- Check previous vote
local old_option = redis.call("GET", voter_key)


-- same vote → no-op
if old_option == new_option then
    return { "no-op" }
end


-- decrement old vote
if old_option then
    local old_count = redis.call("HGET", votes_key, old_option)

    if old_count and tonumber(old_count) > 0 then
        redis.call("HINCRBY", votes_key, old_option, -1)
    end
end


-- increment new vote
redis.call("HINCRBY", votes_key, new_option, 1)
redis.call("SET", voter_key, new_option, "EX", 86400)

return {"ok"}