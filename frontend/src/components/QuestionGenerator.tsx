import { useState, useEffect } from "react";
import axios from "axios";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Loader2, BookOpen, FileQuestion, Settings } from "lucide-react";
import { useToast } from "@/hooks/use-toast";

interface GeneratedQuestion {
  content: string;
  subject: string;
  parts: string;
  type: string;
}

const QuestionGenerator = () => {
  const [subject, setSubject] = useState("");
  const [parts, setParts] = useState("");
  const [questionType, setQuestionType] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [generatedQuestion, setGeneratedQuestion] = useState<GeneratedQuestion | null>(null);
  const { toast } = useToast();

  const subjects = [
    "Mathematics",
    "Physics", 
    "Chemistry",
    "Biology",
    "History",
    "Geography",
    "Economics",
    "English Literature",
    "Psychology",
    "Computer Science"
  ];

  const partOptions = [
    { value: "single", label: "Single Question" },
    { value: "part-ab", label: "Part A + B" },
    { value: "part-abc", label: "Part A + B + C" },
    { value: "part-abcd", label: "Part A + B + C + D" }
  ];

  const questionTypes = [
    "Multiple Choice",
    "Essay Question",
    "Problem Solving",
    "Data Analysis",
    "Case Study",
    "Research Question",
    "Practical Investigation"
  ];

//   useEffect(() => {
//     const generateEmpty = async () => {
//       try {
//         const response = await axios.post("http://localhost:8000/generate", {});
//         console.log("Generated question:", response.data);
//       } catch (error) {
//         console.error("Error generating question:", error);
//       }
//     };

//   generateEmpty();
// }, []);

  const handleGenerate = async () => {
    if (!subject || !parts || !questionType) {
      toast({
        title: "Missing Information",
        description: "Please select all options before generating a question.",
        variant: "destructive"
      });
      return;
    }

    setIsLoading(true);
    
    try {
      // Simulate API call for demo purposes
      await new Promise(resolve => setTimeout(resolve, 2000));
      
      // Mock response - in real app this would be the actual API call
      const mockQuestion: GeneratedQuestion = {
        content: `Here is a sample IB ${subject} question with ${parts.replace('-', ' ')} structure as a ${questionType}:\n\nThis would be the generated question content based on your specifications. The actual implementation would make a POST request to your AI service with the selected parameters.`,
        subject,
        parts,
        type: questionType
      };
      
      setGeneratedQuestion(mockQuestion);
      
      toast({
        title: "Question Generated!",
        description: "Your IB question has been successfully created."
      });
      
    } catch (error) {
      toast({
        title: "Generation Failed",
        description: "There was an error generating your question. Please try again.",
        variant: "destructive"
      });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-subtle">
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
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                {/* Subject Selection */}
                <div className="space-y-2">
                  <label className="text-sm font-medium text-foreground">Subject</label>
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

                {/* Parts Selection */}
                <div className="space-y-2">
                  <label className="text-sm font-medium text-foreground">Question Parts</label>
                  <Select value={parts} onValueChange={setParts}>
                    <SelectTrigger className="bg-background/50">
                      <SelectValue placeholder="Select parts" />
                    </SelectTrigger>
                    <SelectContent className="bg-popover border shadow-medium">
                      {partOptions.map((option) => (
                        <SelectItem key={option.value} value={option.value}>
                          {option.label}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>

                {/* Question Type Selection */}
                <div className="space-y-2">
                  <label className="text-sm font-medium text-foreground">Question Type</label>
                  <Select value={questionType} onValueChange={setQuestionType}>
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
                    {generatedQuestion.subject}
                  </span>
                  <span className="px-3 py-1 bg-accent/10 text-accent rounded-full text-sm">
                    {partOptions.find(p => p.value === generatedQuestion.parts)?.label}
                  </span>
                  <span className="px-3 py-1 bg-secondary text-secondary-foreground rounded-full text-sm">
                    {generatedQuestion.type}
                  </span>
                </div>
              </CardHeader>
              <CardContent>
                <div className="bg-muted/30 rounded-lg p-6 border border-border/50">
                  <pre className="whitespace-pre-wrap text-foreground leading-relaxed">
                    {generatedQuestion.content}
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