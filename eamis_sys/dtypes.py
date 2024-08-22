from typing import TypedDict, Optional

'''
没人问我，但你根本想不到写好Type Hint之后IDE提示多方便
'''

class LessonArrangeInfo(TypedDict):
    weekDay: int
    weekState: str
    startUnit: int
    endUnit: int
    weekStateDigest: str
    startTime: int
    endTime: int
    expLessonGroup: Optional[str]
    expLessonGroupNo: Optional[int]
    roomIds: str
    rooms: str

class LessonData(TypedDict):
    id: int
    no: str
    name: str
    limitCount: int
    planLimitCount: int
    unplanLimitCount: int
    code: str
    credits: int
    courseId: int
    startWeek: int
    endWeek: int
    courseTypeId: int
    courseTypeName: str
    courseTypeCode: str
    scheduled: bool
    hasTextBook: bool
    period: int
    weekHour: int
    withdrawable: bool
    langTypeName: str
    textbooks: str
    teachers: str
    teacherIds: str
    campusCode: str
    campusName: str
    midWithdraw: str
    reservedCount: str
    remark: str
    arrangeInfo: list[LessonArrangeInfo]
    expLessonGroups: list[str]
