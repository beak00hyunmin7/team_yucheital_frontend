#!/usr/bin/env python3
from __future__ import annotations

import math
import sys
from dataclasses import dataclass, field
from enum import Enum
from typing import NamedTuple

MAX_TURN = 200          # maximum turn (days)
START_GOLD = 500        # initial gold
START_WARRIORS = 3      # initial warriors
MOVE_COST = 10          # move cost
TRAIN_COST = 120        # train cost
WORK_INCOME = 15        # income per warrior
UPKEEP_PER_WARRIOR = 2  # upkeep per warrior
HQ_MAX_LEVEL = 5        # HQ max level
BASE_MAX_LEVEL = 3      # base max level
HQ_HEAL_COST = 1000     # HQ fix cost
BASE_HEAL_COST = 500    # base fix cost


class HqLevelEntry(NamedTuple):
    upgrade_cost: int
    warrior_hp: int
    hp: int
    turret: int
    train_cap: int
    work_cap: int


class BaseLevelEntry(NamedTuple):
    cost: int
    hp: int
    turret: int
    work_cap: int


HQ_LEVELS: tuple[HqLevelEntry, ...] = (
    HqLevelEntry(0,     0, 0,  0, 0, 0),
    HqLevelEntry(0,     4, 10, 1, 1, 1),
    HqLevelEntry(600,   5, 15, 2, 1, 2),
    HqLevelEntry(1200,  6, 20, 2, 2, 3),
    HqLevelEntry(2400,  7, 25, 3, 2, 4),
    HqLevelEntry(3600,  8, 30, 3, 3, 5),
)
BASE_LEVELS: tuple[BaseLevelEntry, ...] = (
    BaseLevelEntry(0,    0,  0, 0),
    BaseLevelEntry(300,  6, 1, 1),
    BaseLevelEntry(600,  12, 1, 2),
    BaseLevelEntry(1000, 18, 2, 3),
)


class Side(Enum):
    LEFT = "A"
    RIGHT = "B"

    @property
    def opposite(self) -> "Side":
        return Side.RIGHT if self is Side.LEFT else Side.LEFT

    @classmethod
    def from_word(cls, w: str) -> "Side":
        return cls.LEFT if w == "LEFT" else cls.RIGHT

    @classmethod
    def from_char(cls, c: str) -> "Side":
        return cls.LEFT if c == "A" else cls.RIGHT


class BType(Enum):
    HQ = "HQ"
    BASE = "BASE"


class WState(Enum):
    STATIONARY = 0
    MOVING = 1


@dataclass(frozen=True)
class WarriorId:
    side: Side
    num: int

    def __str__(self) -> str:
        return f"{self.side.value}{self.num}"

    @classmethod
    def parse(cls, tok: str) -> "WarriorId":
        assert tok and tok[0] in ("A", "B")
        return cls(Side.from_char(tok[0]), int(tok[1:]))


@dataclass
class Warrior:
    id: WarriorId
    region: int
    hp: int
    state: WState = WState.STATIONARY
    target: int = 0


@dataclass
class Building:
    region: int
    side: Side
    type: BType
    level: int = 1
    hp: int = 10

    def current_hp(self) -> int:
        return HQ_LEVELS[self.level].hp if self.type is BType.HQ else BASE_LEVELS[self.level].hp

    def work_cap(self) -> int:
        return HQ_LEVELS[self.level].work_cap if self.type is BType.HQ else BASE_LEVELS[self.level].work_cap

    def apply_upgrade(self) -> None:
        self.level += 1
        self.hp = self.current_hp()

    def upgrade_cost(self) -> int:
        if self.type is BType.HQ:
            return HQ_LEVELS[self.level + 1].upgrade_cost
        else:
            return BASE_LEVELS[self.level + 1].cost


@dataclass
class GameMap:
    N: int = 0
    K: int = 0
    x: list[int] = field(default_factory=list)
    y: list[int] = field(default_factory=list)
    strongholds: list[int] = field(default_factory=list)
    adj: list[list[int]] = field(default_factory=list)
    my_side: Side = Side.LEFT
    my_hq: int = 0
    opp_hq: int = 0

    def hq_of(self, s: Side) -> int:
        return 0 if s is Side.LEFT else self.N - 1


@dataclass
class GameState:
    gold: int = START_GOLD
    my_countdown: int = 5
    opp_countdown: int = 5
    warriors: list[Warrior] = field(default_factory=list)
    buildings: list[Building] = field(default_factory=list)
    wave_ids: set[WarriorId] = field(default_factory=set)  # 현재 진행 중인 웨이브에 속한 병사 id 집합
    wave_hq_attack_mode: bool | None = None  # 현재 진행 중인 웨이브가 발진할 때 고정된 hq_attack_mode 값
    reinforced_bases: dict[int, int] = field(default_factory=dict)  # region -> 연속 안전 턴수 (차출 조치 완료 상태 추적)
    hq_replacement_needed: set[int] = field(default_factory=set)    # 본진 대체 인력 파견이 필요한 region 목록

    def find_building(self, region: int) -> Building | None:
        return next((b for b in self.buildings if b.region == region), None)

    def find_warrior(self, wid: WarriorId) -> Warrior | None:
        return next((w for w in self.warriors if w.id == wid), None)


@dataclass
class Actions:
    train_n: int = 0
    moves: list[tuple[WarriorId, int]] = field(default_factory=list)
    upgrades: list[int] = field(default_factory=list)


def make_base(region: int, s: Side) -> Building:
    return Building(region, s, BType.BASE, 1, BASE_LEVELS[1].hp)


def readln() -> str:
    line = sys.stdin.readline()
    if not line:
        sys.exit(0)
    return line.rstrip("\n")


def read_tokens() -> list[str]:
    return readln().split()


def parse_init() -> tuple[GameMap, GameState]:
    M = GameMap()

    t = read_tokens()
    assert len(t) >= 2 and t[0] == "READY"
    M.my_side = Side.from_word(t[1])

    t = read_tokens()
    M.N, M.K = int(t[0]), int(t[1])

    M.x = [int(v) for v in read_tokens()]  # x_0 x_1 ... x_{N-1}
    M.y = [int(v) for v in read_tokens()]  # y_0 y_1 ... y_{N-1}

    M.strongholds = sorted(int(v) for v in read_tokens())  # K strongholds

    M.adj = [[] for _ in range(M.N)]
    for r in range(M.N):
        t = read_tokens()  # deg n_1 n_2 ...
        deg = int(t[0])
        M.adj[r] = sorted(int(v) for v in t[1:1 + deg])

    M.my_hq = M.hq_of(M.my_side)
    M.opp_hq = M.hq_of(M.my_side.opposite)

    S = GameState()
    opp = M.my_side.opposite
    for sfx in range(1, START_WARRIORS + 1):
        S.warriors.append(Warrior(WarriorId(M.my_side, sfx), M.my_hq, HQ_LEVELS[1].warrior_hp))
        S.warriors.append(Warrior(WarriorId(opp, sfx), M.opp_hq, HQ_LEVELS[1].warrior_hp))
    S.buildings.append(
        Building(0, Side.LEFT, BType.HQ, 1, HQ_LEVELS[1].hp)
    )
    S.buildings.append(
        Building(M.N - 1, Side.RIGHT, BType.HQ, 1, HQ_LEVELS[1].hp)
    )

    print("OK", flush=True)
    return M, S


def read_turn_start() -> int | None:
    line = readln()
    if line == "FINISH":
        return None
    t = line.split()
    assert t and t[0] == "START"
    return int(t[2])


def read_turn_result(S: GameState, M: GameMap, submitted: Actions) -> None:
    for region in submitted.upgrades:
        b = S.find_building(region)
        if b is None:
            S.gold -= BASE_LEVELS[1].cost
            S.buildings.append(make_base(region, M.my_side))
        else:
            max_level = HQ_MAX_LEVEL if b.type is BType.HQ else BASE_MAX_LEVEL
            if b.level >= max_level:
                cost = HQ_HEAL_COST if b.type is BType.HQ else BASE_HEAL_COST
                S.gold -= cost
                b.hp = b.current_hp()
            else:
                S.gold -= b.upgrade_cost()
                b.apply_upgrade()

    for wid, target in submitted.moves:
        b = S.find_building(target)
        cost = 0 if (b is not None and b.side is M.my_side) else MOVE_COST
        S.gold -= cost
        w = S.find_warrior(wid)
        if w is not None:
            w.state = WState.MOVING
            w.target = target

    S.gold -= TRAIN_COST * submitted.train_n

    line = readln()
    if line == "FINISH":
        sys.exit(0)
    t = line.split()
    assert t and t[0] == "TURN"

    t = read_tokens()
    S.my_countdown = int(t[2])
    S.opp_countdown = int(t[4])

    # UPGRADE
    t = read_tokens()  # "UPGRADE N"
    n = int(t[1])
    for _ in range(n):
        r = read_tokens()  # "<A|B> <region>"
        s = Side.from_char(r[0][0])
        region = int(r[1])
        b = S.find_building(region)
        if b is None:
            S.buildings.append(make_base(region, s))
        elif b.side is not M.my_side:
            max_level = HQ_MAX_LEVEL if b.type is BType.HQ else BASE_MAX_LEVEL
            if b.level >= max_level:
                b.hp = b.current_hp()
            else:
                b.apply_upgrade()

    # TRAIN
    t = read_tokens()  # "TRAIN N"
    n = int(t[1])
    if n > 0:
        ids = read_tokens()
        for i in range(n):
            wid = WarriorId.parse(ids[i])
            hq_region = M.hq_of(wid.side)
            hq_b = S.find_building(hq_region)
            hq_level = hq_b.level if hq_b is not None else 1
            S.warriors.append(Warrior(wid, hq_region, HQ_LEVELS[hq_level].warrior_hp))

    # MOVE
    t = read_tokens()  # "MOVE N"
    n = int(t[1])
    for _ in range(n):
        r = read_tokens()
        wid = WarriorId.parse(r[0])
        region = int(r[1])
        w = S.find_warrior(wid)
        if w is not None:
            w.region = region
            if (wid.side is M.my_side
                    and w.state is WState.MOVING
                    and w.region == w.target):
                w.state = WState.STATIONARY

    # DAMAGE
    t = read_tokens()  # "DAMAGE N"
    n = int(t[1])
    for _ in range(n):
        r = read_tokens()
        wid = WarriorId.parse(r[1])
        damage = int(r[2])
        w = S.find_warrior(wid)
        if w is not None:
            w.hp -= damage
    S.warriors = [w for w in S.warriors if w.hp > 0]

    # SIEGE
    t = read_tokens()  # "SIEGE N"
    n = int(t[1])
    for _ in range(n):
        r = read_tokens()
        region = int(r[1])
        dmg = int(r[2])
        b = S.find_building(region)
        if b is not None:
            b.hp -= dmg
    S.buildings = [b for b in S.buildings if b.hp > 0]

    readln()  # "END"

    income = 0
    for b in S.buildings:
        if b.side is not M.my_side:
            continue
        count = sum(
            1 for w in S.warriors
            if w.id.side is M.my_side and w.region == b.region
        )
        income += WORK_INCOME * min(count, b.work_cap())
    S.gold += income

    alive = sum(1 for w in S.warriors if w.id.side is M.my_side)
    S.gold = max(0, S.gold - UPKEEP_PER_WARRIOR * alive)


@dataclass
class Paths:
    dist: list[list[float]]
    nxt: list[list[int]]


def euclid_ceil(M: GameMap, u: int, v: int) -> float:
    return math.ceil(math.hypot(M.x[u] - M.x[v], M.y[u] - M.y[v]))


def calculate_paths(M: GameMap) -> Paths:
    INF = math.inf
    N = M.N
    dist = [[INF] * N for _ in range(N)]
    nxt = [[-1] * N for _ in range(N)]

    for i in range(N):
        dist[i][i] = 0.0
        nxt[i][i] = i
    for u in range(N):
        for v in M.adj[u]:
            w = euclid_ceil(M, u, v)
            if w < dist[u][v]:
                dist[u][v] = w

    # Floyd-Warshall
    for k in range(N):
        dk = dist[k]
        for u in range(N):
            du = dist[u]
            duk = du[k]
            if duk == INF:
                continue
            for v in range(N):
                cand = duk + dk[v]
                if cand < du[v]:
                    du[v] = cand

    for u in range(N):
        du = dist[u]
        for v in range(N):
            if u == v or du[v] == INF:
                continue
            best_score = INF
            for nb in M.adj[u]:
                if dist[nb][v] == INF:
                    continue
                score = euclid_ceil(M, u, nb) + dist[nb][v]
                if score < best_score:
                    best_score = score
                    nxt[u][v] = nb
    return Paths(dist, nxt)


def next_step(P: Paths, u: int, v: int) -> int:
    """Returns the next step on the path from u to v. Returns -1 if the path is not reachable."""
    return P.nxt[u][v]


def path(P: Paths, u: int, v: int) -> list[int]:
    """Returns the path from u to v as [u, ..., v]. Returns an empty list if the path is not reachable."""
    if P.nxt[u][v] == -1:
        return []
    out = [u]
    while u != v:
        u = P.nxt[u][v]
        out.append(u)
    return out


def emit(a: Actions) -> None:
    out: list[str] = ["COMMAND"]
    for wid, target in a.moves:
        out.append(f"MOVE {wid} {target}")
    for r in a.upgrades:
        out.append(f"UPGRADE {r}")
    if a.train_n > 0:
        out.append(f"TRAIN {a.train_n}")
    out.append("END")
    sys.stdout.write("\n".join(out) + "\n")
    sys.stdout.flush()

ATTACK_WAVE = 5         # 대규모 웨이브 기준 인원 (8명)
ATTACK_TURN = 100       # 총공격 타이밍
MAX_BASES = 2         # 확장할 기지 수 상한
GOLD_RESERVE = 0       # 유지비 방어용 최소 골드 예비비
HQ_RUSH_TURN = 180      # 막판 본진 올인 턴 조건
HQ_MIN_GARRISON = 5     # 웨이브를 보내도 본진에 항상 남겨둘 최소 방어 인원
FIRST_WAVE_DONE = False


def hop_dist_from(M: GameMap, src: int) -> list[int]:
    """src에서 각 구역까지의 홉 수(BFS). 도달 불가면 -1."""
    d = [-1] * M.N
    d[src] = 0
    q = [src]
    for u in q:
        for v in M.adj[u]:
            if d[v] < 0:
                d[v] = d[u] + 1
                q.append(v)
    return d

def pick_next_base(S: GameState, M: GameMap, P: Paths) -> int | None:
    bases = [
        b.region for b in S.buildings
        if b.side is not M.my_side and b.type is BType.BASE
    ]

    if not bases:
        return None

    return min(bases, key=lambda r: P.dist[M.my_hq][r])

def nearest_enemy_base(S: GameState, M: GameMap, P: Paths, src: int) -> int:
    enemy_bases = [
        b for b in S.buildings
        if b.side is not M.my_side and b.type is BType.BASE
    ]
    reachable = [b for b in enemy_bases if P.dist[src][b.region] != math.inf]
    if not reachable:
        return M.opp_hq
    return min(reachable, key=lambda b: P.dist[src][b.region]).region

def decide(S: GameState, M: GameMap, P: Paths, turn: int) -> Actions:
    global FIRST_WAVE_DONE
    
    a = Actions()
    budget = S.gold

    def spend(cost: int, reserve: int = GOLD_RESERVE) -> bool:
        nonlocal budget
        if budget - cost < reserve:
            return False
        budget -= cost
        return True

    my = [w for w in S.warriors if w.id.side is M.my_side]
    enemy = [w for w in S.warriors if w.id.side is not M.my_side]
    my_b = {b.region: b for b in S.buildings if b.side is M.my_side}
    enemy_base_count = sum(1 for b in S.buildings if b.side is not M.my_side and b.type is BType.BASE)
    my_base_count = sum( 1 for b in my_b.values() if b.type is BType.BASE)


    mine_at: dict[int, int] = {}
    for w in my:
        mine_at[w.region] = mine_at.get(w.region, 0) + 1
    enemy_at: dict[int, int] = {}
    for w in enemy:
        enemy_at[w.region] = enemy_at.get(w.region, 0) + 1

    def can_build_at(r: int) -> bool:
        return mine_at.get(r, 0) >= 1 and enemy_at.get(r, 0) == 0

    # endgame/stronger는 조기경보(긴급귀환) 판단보다 먼저 알아야 하므로 여기서 계산
    stronger = len(my) >= len(enemy) + 2

    hq_attack_mode = (turn >= 100 and my_base_count > enemy_base_count)

    hq = my_b.get(M.my_hq)

    enemy_bases_alive = any(
        b.side is not M.my_side and b.type is BType.BASE
        for b in S.buildings
    )
    hq_rush = turn >= HQ_RUSH_TURN and not enemy_bases_alive

    # ---------- 1. 건설 (경제 최우선: 기지 먼저) ----------
    n_bases = sum(1 for b in my_b.values() if b.type is BType.BASE)

    if FIRST_WAVE_DONE:
        MAX_BASES = 100

    else:
        MAX_BASES = min(M.K // 3,    max(1, enemy_base_count+1))

    if hq_rush:
        expansions: list[int] = []
    else:
        expansions = sorted(
            (s for s in M.strongholds
             if S.find_building(s) is None
             and (P.dist[M.my_hq][s] < P.dist[M.opp_hq][s] or mine_at.get(s, 0) > 0)),
            key=lambda s: P.dist[M.my_hq][s],
        )[:max(0, MAX_BASES - n_bases)]
        for s in expansions:
            if can_build_at(s) and spend(BASE_LEVELS[1].cost):
                a.upgrades.append(s)

    my_base_count = sum(
        1 for b in my_b.values()
        if b.type is BType.BASE
    )

    opp_hq = next(
        (
            b for b in S.buildings
            if b.side is not M.my_side and b.type is BType.HQ
        ),
        None
    )

    if hq is not None and can_build_at(M.my_hq) and M.my_hq not in a.upgrades:
        if hq.level < HQ_MAX_LEVEL:
            cost = hq.upgrade_cost()
            
            if hq_rush:
                priority = budget >= cost
            else:
                priority = (
                    my_base_count >= 2
                    and budget >= cost + GOLD_RESERVE
                    and (
                        opp_hq is None
                        or hq.level <= opp_hq.level
                    )
                )

            if priority:
                budget -= cost
                a.upgrades.append(M.my_hq)

        elif hq.hp <= hq.current_hp() // 2 and budget >= HQ_HEAL_COST:
            budget -= HQ_HEAL_COST
            a.upgrades.append(M.my_hq)

    if FIRST_WAVE_DONE:

        my_bases = sorted(
            [
                b for b in my_b.values()
                if b.type is BType.BASE
            ],
            key=lambda b: P.dist[M.my_hq][b.region]
        )

        for b in my_bases[:2]:
            if b.level == 1:
                cost = b.upgrade_cost()

                if spend(cost):
                    a.upgrades.append(b.region)


    # ---------- 2. 병력 배치 ----------
    keep: dict[int, int] = {}

    for r, b in my_b.items():
        keep[r] = b.work_cap()

    for s in expansions:
        keep[s] = 1

    need = {r: max(0, k - mine_at.get(r, 0)) for r, k in keep.items()}
    for w in my:
        if w.state is WState.MOVING and need.get(w.target, 0) > 0:
            need[w.target] -= 1

    surplus: list[Warrior] = []
    workers: list[Warrior] = []
    used: dict[int, int] = {}
    for w in my:
        if w.state is not WState.STATIONARY:
            continue
        if used.get(w.region, 0) < keep.get(w.region, 0):
            used[w.region] = used.get(w.region, 0) + 1
            workers.append(w)
        else:
            surplus.append(w)

    # ---- 웨이브 진행 상태 추적 (건설/주둔으로 남은 인원은 웨이브에서 제외) ----
    # 1) 죽었거나 더 이상 존재하지 않는 병사 제거
    S.wave_ids = {wid for wid in S.wave_ids if S.find_warrior(wid) is not None}
    # 2) 이번 턴에 거점 유지 인력(workers)으로 흡수된 병사는 웨이브에서 제외
    S.wave_ids -= {w.id for w in workers}
    # 3) 1명만 남으면 사실상 웨이브가 끝난 것으로 간주 (그 1명 때문에 다음 웨이브가 막히지 않게)
    wave_running = len(S.wave_ids) > 1

    # ---- [1] 웨이브 목적지 락: 진행 중인 웨이브의 target이 hq_attack_mode 변화로 ----
    # 강제 변경되지 않도록, 웨이브가 진행 중이 아닐 때만 최신 값을 스냅샷 떠서 잠근다.
    if not wave_running:
        S.wave_hq_attack_mode = hq_attack_mode
    effective_hq_attack_mode = S.wave_hq_attack_mode

    def order_move(w: Warrior, dest: int) -> bool:
        if dest == w.region or P.dist[w.region][dest] == math.inf:
            return False
        if dest not in my_b and not spend(MOVE_COST):
            return False
        a.moves.append((w.id, dest))
        return True

    # =========================================================================
    # [2] 지역 거점 방어: 공격받는 아군 기지(BASE)에 가장 가까운 다른 거점에서
    #     일꾼 1명을 차출해 즉시 지원 보내고, 차출로 빈 그 거점 자리는
    #     이후 본진(HQ)에서 대체 인력을 파견해 채운다.
    # =========================================================================
    RESCUE_SAFE_TURNS = 2  # 이 턴수만큼 연속 안전해야 "차출 완료" 상태를 해제(재공격 시 재차출 허용)

    threatened_bases = sorted(
        (
            b for b in my_b.values()
            if b.type is BType.BASE and enemy_at.get(b.region, 0) > 0
        ),
        key=lambda b: (-enemy_at.get(b.region, 0), b.hp),
    )

    # 2-1) 이미 조치(차출)한 기지들의 안전 상태 갱신 — 완전히 안전해지기 전엔 반복 차출하지 않는다
    for region in list(S.reinforced_bases.keys()):
        if region not in my_b:
            del S.reinforced_bases[region]
            continue
        if enemy_at.get(region, 0) > 0:
            S.reinforced_bases[region] = 0  # 아직 위협 중 → 안전 카운터 리셋
        else:
            S.reinforced_bases[region] += 1
            if S.reinforced_bases[region] >= RESCUE_SAFE_TURNS:
                del S.reinforced_bases[region]

    # 2-2) 새로 공격받는(아직 조치하지 않은) 기지마다, 가장 가까운 다른 아군 거점에서 일꾼 1명 차출
    for tb in threatened_bases:
        if tb.region in S.reinforced_bases:
            continue  # 이미 차출 조치를 취해서 대응 중인 기지 → 반복 차출 안 함

        donor_candidates = [
            w for w in workers
            if w.region != tb.region and w.region != M.my_hq and w.region in my_b
        ]
        if not donor_candidates:
            continue

        donor = min(donor_candidates, key=lambda w: P.dist[w.region][tb.region])
        if order_move(donor, tb.region):
            workers.remove(donor)
            S.reinforced_bases[tb.region] = 0
            S.hq_replacement_needed.add(donor.region)  # 차출로 빈 자리는 본진에서 채워야 함

    # 2-3) 본진에서 대체 인력 파견 (차출 때문에 빈 거점 자리를 다시 채움)
    for region in list(S.hq_replacement_needed):
        if region not in my_b:
            S.hq_replacement_needed.discard(region)
            continue
        if mine_at.get(region, 0) >= my_b[region].work_cap():
            S.hq_replacement_needed.discard(region)  # 다른 경로로 이미 채워짐
            continue
        replacement = next((w for w in surplus if w.region == M.my_hq), None)
        if replacement is None:
            continue  # 본진에 보낼 여유 인력이 아직 없음 — 다음 기회에 재시도
        if order_move(replacement, region):
            surplus.remove(replacement)
            S.hq_replacement_needed.discard(region)
    # =========================================================================


    # =========================================================================
    # [수정] 도달 턴수(Turn-to-Arrival) 예측 조기 경보 방어 시스템 (대형 맵 대응)
    # =========================================================================
    # 우리 병력이 본진으로 복귀하는 데 걸리는 최장 홉(Hop) 수 계산
    hops_to_hq = hop_dist_from(M, M.my_hq)
    max_my_return_hop = 1
    for w in my:
        if hops_to_hq[w.region] > max_my_return_hop:
            max_my_return_hop = hops_to_hq[w.region]

    # 본진 수비를 위해 조기 대피를 발령해야 하는 유동적 위험 한계선 설정
    # 안전 마진(+1~2턴)을 부여하여 아군이 먼저 도착해 벽을 치도록 유도
    buffer_turns = max_my_return_hop + 2

    hq_attackers = 0
    for w in enemy:
        dist_to_my_hq = P.dist[w.region][M.my_hq]
        if dist_to_my_hq != math.inf:
            # 적이 우리 본진까지 진격하는 데 걸리는 대략적인 물리적 턴수 예측
            # (한 칸당 평균 가중치 이동 효율 고려)
            estimated_turns_to_arrive = dist_to_my_hq / 15.0
            
            # 아군이 복귀 완료하기 전 혹은 직후에 적이 본진에 도달하는 범위 내에 있으면 카운트
            if estimated_turns_to_arrive <= buffer_turns:
                hq_attackers += 1

    # 상대의 분산 압박(6~7인조 분할 찌르기 등) 로그 피드백을 반영해 조건 완화 (6인 이상)
    is_hq_under_attack = hq_attackers >= 5 or enemy_at.get(M.my_hq, 0) >= 2

    if is_hq_under_attack and not hq_attack_mode:
        # 비상 소환 명령: 전 맵의 일꾼과 유휴 병력을 지체 없이 본진으로 강제 철수
        # (endgame일 때는 긴급귀환에 영향받지 않고 무조건 본진 공격을 계속함)
        all_moveable_warriors = surplus + workers
        for w in all_moveable_warriors:
            if w.region != M.my_hq:
                order_move(w, M.my_hq)
        
        # 기동 대기열을 완전히 비워 타 기지로의 무의식적 분산을 방지
        surplus = []
        workers = []

    threat = hq_attackers if (is_hq_under_attack and not hq_attack_mode) else 0
    hold = 0
    # =========================================================================

    hq_surplus = sum(
        1 for w in surplus
        if w.region == M.my_hq
    )

    # 새 웨이브는 이전 웨이브가 완전히 소진(전멸/도착/거점 편입)됐을 때만 발진
    
    if not FIRST_WAVE_DONE:
        wave_ready = (
            mine_at.get(M.my_hq, 0) >= 5
            and not wave_running
        )
    else:
        wave_ready = (
            hq_surplus >= ATTACK_WAVE
            and stronger
            and not wave_running
        )

    # 조기 경보(threat > 0) 상황이 아니라면 중간 조우에 쫄지 않고 진격 유지
    # endgame은 threat가 위에서 이미 0으로 고정되므로 긴급귀환과는 무관하게 공격하되,
    # 직전에 보낸 웨이브(엔드게임 웨이브 포함)가 아직 살아있으면 새 웨이브는 보내지 않음
    attack = (wave_ready or (hq_attack_mode and not wave_running)) and (threat == 0 or stronger)

    # HQ에서 실제로 내보낼 인원수를 제한 (최소 방어 인원은 항상 잔류)
    # - 평시 신규 웨이브: 한 턴에 최대 ATTACK_WAVE 명까지만 송출
    # - 막판 endgame: 적 본진 수비 인원을 압도할 수 있을 만큼 골드가 모였을 때만 총력전
    if not attack:
        hq_send_limit = 0
    elif effective_hq_attack_mode:
        desired = max(0, mine_at.get(M.my_hq, 0) - 5)
        # 지금 예비비를 남기고도 낼 수 있는 골드로 몇 명이나 이동시킬 수 있는지 계산
        affordable = max(0, budget - GOLD_RESERVE) // MOVE_COST
        enemy_hq_garrison = enemy_at.get(M.opp_hq, 0)
        if affordable < enemy_hq_garrison:
            # 보낼 수 있는 인원이 상대 본진 수비 병력보다 적으면 전멸당할 뿐이니
            # 골드가 더 모일 때까지 대기 (웨이브 미발진)
            hq_send_limit = 0
        else:
            hq_send_limit = min(desired, hq_surplus, affordable)
    else:
        hq_send_limit = ATTACK_WAVE#min(max(0, hq_surplus - HQ_MIN_GARRISON), ATTACK_WAVE)
    hq_sent = 0

    # ---- 웨이브 및 잉여 병력 목적지 제어 ----
    for w in surplus:
        # endgame에서는 기지 경유 없이 무조건 적 본진을 목표로 진격
        # (진행 중인 웨이브라면 hq_attack_mode가 이번 턴에 바뀌어도 웨이브 시작 시 고정된 값을 사용)
        target = M.opp_hq if effective_hq_attack_mode else nearest_enemy_base(S, M, P, w.region)
        
        if hold > 0 and w.region == M.my_hq:
            hold -= 1  
            continue

        if w.region != M.my_hq and (threat == 0 or stronger):
            if w.region == target:
                continue  
            if order_move(w, target):
                S.wave_ids.add(w.id)
                continue

        if attack and w.region == M.my_hq:
            if hq_sent < hq_send_limit:
                if order_move(w, target):
                    S.wave_ids.add(w.id)
                    hq_sent += 1

                    if not FIRST_WAVE_DONE:
                        FIRST_WAVE_DONE = True
            # 한도를 넘긴 인원은 이동시키지 않고 본진에 방어 병력으로 잔류
            continue
        
        # 복귀 시스템: 본진 긴급 사태가 해제되면 공백이 생긴 일터로 차례대로 복귀
        empty = [r for r, n in need.items() if n > 0]
        if empty:
            dest = min(empty, key=lambda r: P.dist[w.region][r])
            if order_move(w, dest):
                need[dest] -= 1
                continue
        if w.region != M.my_hq:
            order_move(w, M.my_hq)

    # endgame에서도 거점 유지 인력(workers)은 건드리지 않음 — surplus 웨이브 규모만 커짐

    # ---------- 3. 훈련 (미착공 확장의 건설비를 먼저 격리) ----------
    if hq is not None:
        covered = {
            s for s in expansions
            if mine_at.get(s, 0) > 0
            or any(w.state is WState.MOVING and w.target == s for w in my)
            or any(d == s for _, d in a.moves)
        }
        pending = sum(BASE_LEVELS[1].cost for s in covered if s not in a.upgrades)
        if hq_rush:
            if hq.level < HQ_MAX_LEVEL and M.my_hq not in a.upgrades:
                pending += hq.upgrade_cost()
            cap = 0 if len(my) >= 3 else HQ_LEVELS[hq.level].train_cap
        else:
            if ((hq.level < 5 and (
                        opp_hq is None
                        or hq.level <= opp_hq.level
                    )) and not expansions and len(my) >= 8
                    and M.my_hq not in a.upgrades):
                pending += hq.upgrade_cost()
            cap = HQ_LEVELS[hq.level].train_cap
        reserve = 0 if len(my) < 3 else GOLD_RESERVE + pending  
        while a.train_n < cap and spend(TRAIN_COST, reserve):
            a.train_n += 1

    return a


def main() -> None:
    M, S = parse_init()
    P = calculate_paths(M)

    while (turn := read_turn_start()) is not None:
        a = decide(S, M, P, turn)
        emit(a)
        read_turn_result(S, M, a)


if __name__ == "__main__":
    main()