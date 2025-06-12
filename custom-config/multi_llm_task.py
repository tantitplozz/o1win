from typing import Any, Dict, List, Protocol, Type, TypeVar


class TaskProtocol(Protocol):
    """Protocol defining the interface for Task objects"""

    id: str

    def __init__(self, **kwargs) -> None: ...
    def validate(self) -> bool: ...
    def execute(self, **kwargs) -> Dict[str, Any]: ...


class PipelineProtocol(Protocol):
    """Protocol defining the interface for Pipeline objects"""

    id: str

    def __init__(self, **kwargs) -> None: ...
    def run(self, **kwargs) -> Dict[str, Any]: ...
    def validate(self) -> bool: ...


T = TypeVar("T", bound=TaskProtocol)
P = TypeVar("P", bound=PipelineProtocol)


def get_implementation_classes() -> tuple[Type[TaskProtocol], Type[PipelineProtocol]]:
    """Get the Task and Pipeline implementations (real or mock)"""
    try:
        from openhands import Pipeline, Task

        return Task, Pipeline
    except ImportError:
        # Mock classes for development
        class MockTask:
            """Mock Task implementation"""

            def __init__(self, **kwargs) -> None:
                self.id = kwargs.get("id", "")
                self._config = kwargs

            def validate(self) -> bool:
                return True

            def execute(self, **kwargs) -> Dict[str, Any]:
                return {"status": "mock", "task": self.id, "input": kwargs}

        class MockPipeline:
            """Mock Pipeline implementation"""

            def __init__(self, **kwargs) -> None:
                self.id = kwargs.get("id", "")
                self._config = kwargs
                self._tasks = kwargs.get("tasks", [])

            def run(self, **kwargs) -> Dict[str, Any]:
                return {"status": "mock", "pipeline": self.id, "input": kwargs}

            def validate(self) -> bool:
                return True

        return MockTask, MockPipeline


# Get implementation classes
TaskImpl, PipelineImpl = get_implementation_classes()


def create_multi_llm_pipeline() -> PipelineProtocol:
    """Creates a pipeline for handling multi-LLM requests"""
    # Task หลักสำหรับเรียก Multi-LLM API
    multi_llm_task = TaskImpl(
        id="multi_llm_task",
        description="เรียก multi-LLM API",
        uses="http.request",
        with_={
            "method": "POST",
            "url": "http://localhost:8000/llm/multi-llm",
            "headers": {"Content-Type": "application/json"},
            "body": {
                "prompt": "{{ input.prompt }}",
                "models": ["dolphin", "yi", "mythomax"],
            },
        },
        outputs={"results": "{{ outputs.response.results }}"},
        on_error={
            "retry": {
                "max_attempts": 3,
                "initial_delay": 1,
                "max_delay": 5,
                "multiplier": 2,
            }
        },
        timeout=60,
    )

    # Task สำหรับประมวลผลคำตอบ
    def process_responses(model_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        processed_responses = {}
        for model_result in model_results:
            model = model_result["model"]
            response = model_result["response"]
            processed_responses[model] = response
        return processed_responses

    process_task = TaskImpl(
        id="process_responses",
        description="ประมวลผลและเปรียบเทียบคำตอบจาก LLM",
        uses="python",
        needs=[multi_llm_task.id],
        with_={"code": process_responses},
    )

    # สร้าง Pipeline
    return PipelineImpl(
        id="multi_llm_pipeline",
        description="Pipeline สำหรับเรียกใช้งาน Multi-LLM และประมวลผล",
        tasks=[multi_llm_task, process_task],
    )


# ตัวอย่างการใช้งาน
if __name__ == "__main__":
    pipeline = create_multi_llm_pipeline()
    pipeline_result = pipeline.run(inputs={"prompt": "สรุปกลยุทธ์การพัฒนา AI ในปี 2024"})
    print(pipeline_result)
