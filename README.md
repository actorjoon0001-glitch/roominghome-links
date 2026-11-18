# 링크 모음 페이지 템플릿 (link-page-template)

쇼츠·릴스 시청자가 **"프로필 링크 → N번 상품"** 으로 들어와 쿠팡 파트너스 링크를 누르는 한 페이지 사이트예요.
인포크링크 같은 링크 모음을 서버 없이 GitHub Pages로 무료 운영합니다.

- 모바일 우선, 프레임워크 없는 정적 HTML 한 장 (`index.html`)
- 브랜드별 값은 **`config.json`** 하나, 상품 목록은 **`products.json`** 하나만 고치면 끝
- `주소/#3` → 3번 카드로 스크롤 + 하이라이트
- 상품명·태그·번호 검색, 태그 필터 칩
- 쿠팡 버튼은 새 탭 + `rel="sponsored noopener"`, 상단에 파트너스 고지문 고정

## 새 브랜드 추가하는 법

### 1. 템플릿으로 레포 만들기
이 레포 위쪽 초록색 **Use this template → Create a new repository**
- 이름 예: `브랜드명-links` · **Public** 으로 만들기 (무료 Pages는 공개 레포만 가능)

### 2. `config.json` 고치기 (GitHub 웹에서 연필 아이콘으로 수정해도 돼요)

| 키 | 뜻 |
|---|---|
| `brand.name` | 브랜드명 (제목·공유 미리보기에 쓰임) |
| `brand.tagline` | 한 줄 소개 |
| `brand.logo` | 로고 이미지 경로 (`assets/logo.png` 를 교체하면 그대로 둬도 됨). 파비콘으로도 쓰임 |
| `brand.og_image` | 카톡·인스타 공유 미리보기 이미지 (1200×630 권장). 없으면 로고 사용 |
| `colors.background` / `surface` | 배경 / 카드 배경 |
| `colors.primary` / `on_primary` | 메인 색(번호 뱃지·구매 버튼) / 그 위 글자색 |
| `colors.secondary` | 보조 색(태그·영상 링크) |
| `colors.text` / `muted` | 본문 글자 / 흐린 글자 |
| `fonts.title` / `fonts.body` | 구글 폰트 이름 (예: `Black Han Sans`, `Nanum Gothic`) |
| `social.youtube` / `instagram` / `tiktok` | 채널 주소. **비워두면 버튼이 안 보여요** |
| `disclosure` | 쿠팡 파트너스 고지 문구 (비우면 고지 박스가 사라지니 **반드시 넣으세요**) |
| `domain` | 커스텀 도메인 (예: `example.com`). 비우면 `아이디.github.io/레포명` 주소 사용 |
| `texts.*` | 버튼·안내 문구 (`price_basis` 의 `{date}` 는 상품 날짜로 바뀜) |
| `sort` | `desc` = 최신 번호가 위 / `asc` = 1번부터 |

### 3. `products.json` 고치기
```json
{ "items": [
  { "no": 1, "tags": ["겨울", "단열"], "name": "상품명", "price": 12900, "price_label": "쿠팡 판매가",
    "date": "2026-11-18", "image": "assets/products/1.jpg", "link": "https://link.coupang.com/a/xxxx", "video": "" }
]}
```
- `no` 번호는 영상에서 말한 번호와 같게, 한 번 정하면 바꾸지 마세요 (`/#번호` 링크가 깨져요)
- `price` 를 비우거나 0이면 가격을 숨겨요. `date` 가 있으면 "업로드 시점(YYYY.MM.DD) 기준" 표시
- `link` 가 비어 있으면 버튼이 "링크 준비 중"으로 보여요
- `video` 에 쇼츠 주소를 넣으면 "영상 보기" 링크가 생겨요
- 사진은 `assets/products/` 에 올리기 (정사각형 600px 정도, jpg 권장)

### 4. CNAME(커스텀 도메인) 설정
1. `config.json` 의 `domain` 에 도메인 입력 → 저장하면 GitHub Actions가 **`CNAME` 파일과 공유 미리보기 주소를 자동 생성**해요 (Actions 탭에서 초록 체크 확인)
2. 도메인 산 곳(가비아 등) DNS 관리에서 아래처럼 등록
   - `@` (루트) **A 레코드** 4개: `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`
   - `www` **CNAME 레코드**: `아이디.github.io`
3. DNS 반영까지 몇 분~몇 시간 걸려요

### 5. Pages 켜기
레포 **Settings → Pages**
- Source: **Deploy from a branch** · Branch: **main** / **(root)** → Save
- Custom domain 칸에 도메인이 들어가 있는지 확인 (CNAME 파일이 있으면 자동) → DNS 확인되면 **Enforce HTTPS** 체크

1~2분 뒤 `https://도메인/` (또는 `https://아이디.github.io/레포명/`) 에서 확인. 쇼츠 설명란·프로필 링크에 이 주소를 넣으면 끝.

## 직접 확인 / 고급
```bash
python3 tools/sync_config.py          # config.json → index.html head + CNAME (Actions가 대신 해줌)
python3 -m http.server 8000           # http://localhost:8000 에서 미리보기
```
- 공유 미리보기(OG)는 자바스크립트를 안 읽어서 `index.html` 의 `CONFIG:HEAD` 구간에 직접 써넣어야 해요. 그 구간은 자동 생성이니 손으로 고치지 마세요.
- 자동화 파이프라인이 있다면 `products.json` 을 만들어 push 하기만 하면 페이지가 갱신돼요.
