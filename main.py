"""2026 전주대 대동제 & 해커톤 로그에서 정규표현식으로 데이터 추출."""

from pathlib import Path
import re

LOG_FILE = Path(__file__).resolve().parent / "07-02. 전주대 대동제 및 해커톤 통합운영 데이터 로그.txt"


def extract_emails(text):
    # @ 뒤의 도메인은 점으로 구분된 정상적인 이름이 있어야 한다.
    pattern = r"(?<![\w.@-])[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)+(?![\w.-])"
    return re.findall(pattern, text)


def extract_phones(text):
    # 010 + 구분자(-, ., 공백) + 숫자 4자리 + 구분자 + 숫자 4자리
    pattern = r"(?<!\d)010[-. ]\d{4}[-. ]\d{4}(?!\d)"
    return re.findall(pattern, text)


def extract_students(text):
    # '[학번 / 학과]' 중 202로 시작하는 9자리 학번만 추출한다.
    pattern = r"\[\s*(202\d{6})\s*/\s*([^\]\r\n]+?)\s*\]"
    return re.findall(pattern, text)


def extract_github_urls(text):
    # GitLab은 제외하고 github.com의 사용자명/저장소명 URL만 찾는다.
    pattern = r"https?://github\.com/[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+(?:\.git)?(?=$|[\s)\]])"
    return re.findall(pattern, text, flags=re.MULTILINE)


def extract_coupons(text):
    # 발급 연도가 2026년이고 뒤에 영문 대문자/숫자 4글자가 오는 코드
    pattern = r"(?<![A-Za-z0-9-])FEST-2026-[A-Z0-9]{4}(?![A-Za-z0-9-])"
    return re.findall(pattern, text)


def extract_sales(text):
    # 한 줄의 '매출:' 바로 뒤 금액만 찾아 카드/현금 세부 내역은 제외한다.
    pattern = r"^\s*-\s*(.+?)\s+매출:\s*([\d,]+)원"
    matches = re.findall(pattern, text, flags=re.MULTILINE)
    return [(booth, int(amount.replace(",", ""))) for booth, amount in matches]


def main():
    try:
        text = LOG_FILE.read_text(encoding="utf-8-sig")
    except FileNotFoundError:
        print(f"로그 파일을 찾을 수 없습니다: {LOG_FILE}")
        return

    emails = extract_emails(text)
    phones = extract_phones(text)
    students = extract_students(text)
    github_urls = extract_github_urls(text)
    coupons = extract_coupons(text)
    sales = extract_sales(text)

    print("=" * 55)
    print("2026 전주대학교 대동제 & 해커톤 통합 로그 분석")
    print("=" * 55)

    print(f"\n[1] 유효한 이메일 ({len(emails)}개)")
    for email in emails:
        print(" -", email)

    print(f"\n[2] 유효한 휴대폰 번호 ({len(phones)}개)")
    for phone in phones:
        print(" -", phone)

    print(f"\n[3] 본교 재학생 (학번, 학과) ({len(students)}개)")
    for student in students:
        print(" -", student)

    print(f"\n[4-1] GitHub 저장소 URL ({len(github_urls)}개)")
    for url in github_urls:
        print(" -", url)

    print(f"\n[4-2] 2026년도 유효 쿠폰 코드 ({len(coupons)}개)")
    for coupon in coupons:
        print(" -", coupon)

    print("\n[5] 부스별 총 매출액")
    for booth, amount in sales:
        print(f" - {booth}: {amount:,}원")
    print(f" 전체 매출 합계: {sum(amount for _, amount in sales):,}원")


if __name__ == "__main__":
    main()
