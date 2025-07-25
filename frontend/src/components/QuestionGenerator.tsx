import { useState, useEffect } from "react";
import axios from "axios";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Loader2, BookOpen, FileQuestion, Settings } from "lucide-react";
import { useToast } from "@/hooks/use-toast";

interface QuestionPart {
  content: string;
  markscheme: string;
  order: number;
  marks?: number;
  subtopics?: string[];
}

interface Option {
  content: string;
  correct: boolean;
  markscheme: string;
  order: number;
  subtopics?: string[];
}

interface GeneratedQuestion {
  id: string;
  parts: QuestionPart[];
  options: Option[];
}

const QuestionGenerator = () => {
  const [subject, setSubject] = useState("");
  const [topic, setTopic] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [generatedQuestion, setGeneratedQuestion] =
    useState<GeneratedQuestion | null>(null);
  const { toast } = useToast();

  const subjects = ["Mathematics", "Computer Science"];

  const partOptions = [
    { value: "single", label: "Single Question" },
    { value: "part-ab", label: "Part A + B" },
    { value: "part-abc", label: "Part A + B + C" },
    { value: "part-abcd", label: "Part A + B + C + D" },
  ];

  const questionTypes =
    subject === "Mathematics"
      ? [
          "Number and Algebra",
          "Functions",
          "Geometry and Trigonometry",
          "Statistics and Probability",
          "Calculus",
        ]
      : subject === "Computer Science"
      ? ["Not yet"]
      : ["Please select a subject first"];

  const handleGenerate = async () => {
    if (!subject || !topic) {
      toast({
        title: "Missing Information",
        description: "Please select all options before generating a question.",
        variant: "destructive",
      });
      return;
    }

    setGeneratedQuestion(null);
    setIsLoading(true);

    try {
      const response = await axios.post(
        "http://127.0.0.1:8000/generate",
        {
          subject: subject,
          topic: topic,
        },
        {
          headers: {
            "Content-Type": "application/json",
          },
        }
      );

      // Extract the generated question from response
      const generatedQuestion: GeneratedQuestion = {
        id: response.data.id,
        parts: response.data.parts,
        options: response.data.options,
      };

      setGeneratedQuestion(generatedQuestion);

      toast({
        title: "Question Generated!",
        description: "Your IB question has been successfully created.",
      });
    } catch (error) {
      console.error("API Error:", error);

      let errorMessage =
        "There was an error generating your question. Please try again.";

      if (axios.isAxiosError(error)) {
        if (error.code === "ECONNABORTED") {
          errorMessage = "Request timed out. Please try again.";
        } else if (error.response?.status === 400) {
          errorMessage =
            "Invalid request parameters. Please check your selections.";
        } else if (error.response?.status === 500) {
          errorMessage = "Server error. Please try again later.";
        } else if (error.response?.data?.message) {
          errorMessage = error.response.data.message;
        }
      }

      toast({
        title: "Generation Failed",
        description: errorMessage,
        variant: "destructive",
      });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-subtle pt-16">
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <div className="text-center mb-12">
          <div className="flex items-center justify-center gap-3 mb-4">
            <BookOpen className="h-10 w-10 text-primary" />
            <h1 className="text-4xl font-bold bg-gradient-primary bg-clip-text text-transparent">
              IB AI Question Generator
            </h1>
          </div>
          <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
            Math AA + CS Demo
          </p>
        </div>

        <div className="max-w-4xl mx-auto space-y-8">
          {/* Configuration Card */}
          <Card className="shadow-medium border-0 bg-card/80 backdrop-blur-sm">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Settings className="h-5 w-5" />
                Question Configuration
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-6">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {/* Subject Selection */}
                <div className="space-y-2">
                  <label className="text-sm font-medium text-foreground">
                    Subject
                  </label>
                  <Select value={subject} onValueChange={setSubject}>
                    <SelectTrigger className="bg-background/50">
                      <SelectValue placeholder="Select subject" />
                    </SelectTrigger>
                    <SelectContent className="bg-popover border shadow-medium">
                      {subjects.map((sub) => (
                        <SelectItem key={sub} value={sub}>
                          {sub}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>

                {/* Topic Selection */}
                <div className="space-y-2">
                  <label className="text-sm font-medium text-foreground">
                    Topic
                  </label>
                  <Select value={topic} onValueChange={setTopic}>
                    <SelectTrigger className="bg-background/50">
                      <SelectValue placeholder="Select type" />
                    </SelectTrigger>
                    <SelectContent className="bg-popover border shadow-medium">
                      {questionTypes.map((type) => (
                        <SelectItem key={type} value={type}>
                          {type}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>
              </div>

              {/* Generate Button */}
              <div className="flex justify-center pt-4">
                <Button
                  onClick={handleGenerate}
                  disabled={isLoading}
                  className="bg-gradient-primary hover:opacity-90 px-8 py-6 text-lg font-semibold shadow-medium"
                >
                  {isLoading ? (
                    <>
                      <Loader2 className="mr-2 h-5 w-5 animate-spin" />
                      Generating Question...
                    </>
                  ) : (
                    <>
                      <FileQuestion className="mr-2 h-5 w-5" />
                      Generate
                    </>
                  )}
                </Button>
              </div>
            </CardContent>
          </Card>

          {/* Generated Question Display */}
          {generatedQuestion && (
            <Card className="shadow-medium border-0 bg-card/80 backdrop-blur-sm">
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <FileQuestion className="h-5 w-5" />
                  Generated Question
                </CardTitle>
                <div className="flex flex-wrap gap-2">
                  <span className="px-3 py-1 bg-primary/10 text-primary rounded-full text-sm">
                    {generatedQuestion.id}
                  </span>

                  <span className="px-3 py-1 bg-secondary text-secondary-foreground text-sm">
                    <div className="space-y-2">
                      {generatedQuestion.parts.map((part, idx) => (
                        <div
                          key={idx}
                          className="px-3 py-2 bg-secondary text-secondary-foreground text-sm"
                        >
                          <p>
                            <strong>Content:</strong> {part.content}
                          </p>
                          <p>
                            <strong>Marks:</strong> {part.marks}
                          </p>
                          <p>
                            <strong>Markscheme:</strong> {part.markscheme}
                          </p>
                          <p>
                            <strong>Subtopics:</strong>{" "}
                            {part.subtopics.join(", ")}
                          </p>
                          <p>
                            <strong>Order:</strong> {part.order}
                          </p>
                        </div>
                      ))}
                    </div>
                  </span>
                </div>
              </CardHeader>
              <CardContent>
                <div className="bg-muted/30 rounded-lg p-6 border border-border/50">
                  <pre className="whitespace-pre-wrap text-foreground leading-relaxed">
                    {generatedQuestion.options
                      .map((part, idx) => part.content)
                      .join(", ")}
                  </pre>
                </div>
              </CardContent>
            </Card>
          )}
        </div>
      </div>
    </div>
  );
};

export default QuestionGenerator;
