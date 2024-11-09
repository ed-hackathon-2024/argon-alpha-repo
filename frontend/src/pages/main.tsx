import {
  Button,
  Chip,
  Divider,
  IconButton,
  MenuItem,
  Select,
  Stack,
  styled,
  TextField,
  Typography,
} from "@mui/material";
import ArrowBackIosIcon from "@mui/icons-material/ArrowBackIos";
import InfoOutlinedIcon from "@mui/icons-material/InfoOutlined";
import SendOutlinedIcon from "@mui/icons-material/SendOutlined";
import ClearIcon from "@mui/icons-material/Clear";
import { useMemo, useState } from "react";
import { PieChart } from "@mui/x-charts";
import { Check } from "@mui/icons-material";
import DeleteIcon from "@mui/icons-material/Delete";

export function MainPage() {
  const [selectedCategories, setSelectedCategories] = useState<
    CategoryDetails[]
  >([]);
  const [availableCategories, setAvailableCategories] = useState<string[]>([]);
  const [categoriesDetails, setCategoriesDetails] = useState<CategoryDetails[]>(
    []
  );

  const saved = selectedCategories.reduce(
    (acc, item) => acc + item.chart.current - item.chart.goal,
    0
  );

  const api_url = "https://f1c4-147-232-172-12.ngrok-free.app";

  const handleFirstRequest = async (value: string) => {
    const categories = await fetch(`${api_url}/api/get_categories_activity/`, {
      headers: {
        "ngrok-skip-browser-warning": "69420",
      },
    })
      .then((response) => response.json())
      .then((data) => {
        const items = data.categories.map((item: any) => item?.category);

        data.categories.map((item: any) => {
          setAvailableCategories(items.slice(0, 10));
        });

        return data.categories;
      });

    categories
      ?.slice(0, 10)
      .map((item: { category: string; total_price: number }) => {
        fetch(`${api_url}/api/get_category_contente/`, {
          method: "POST",
          headers: {
            "ngrok-skip-browser-warning": "69420",
          },
          body: JSON.stringify({
            user_goal: value,
            category_name: item.category,
          }),
        })
          .then((response) => response.json())
          .then((data) => {
            setCategoriesDetails((prev) => [
              ...prev,
              {
                name: item.category,
                description: data.overview + " || Overview: " + data.overview,
                chart: {
                  current: item.total_price,
                  goal: data.goal,
                },
              },
            ]);
          });
      });
  };

  return (
    <Page>
      <Container>
        <Header />
        <StatsCard saved={saved} total={200} />
        <Content
          onSubmit={handleFirstRequest}
          categoriesList={availableCategories}
          selectedCategories={selectedCategories}
          setSelectedCategories={setSelectedCategories}
          categoriesDetails={categoriesDetails}
        />
      </Container>
    </Page>
  );
}

function Header() {
  return (
    <Stack
      direction="row"
      justifyContent="space-between"
      sx={{ background: "#FF6130", p: "24px 20px", height: "125px" }}
    >
      <ArrowBackIosIcon sx={{ color: "#fff", fontSize: "24px" }} />
      <InfoOutlinedIcon sx={{ color: "#fff", fontSize: "24px" }} />
    </Stack>
  );
}

function StatsCard({ saved, total }: { saved: number; total: number }) {
  return (
    <Stack
      sx={{
        p: "16px 0px 10px 0px",
        borderRadius: "8px",
        boxShadow: "0px 4px 30px 0px rgba(0, 0, 0, 0.04)",
        backgroundColor: "#fff",
        width: "90%",
        m: "-65px auto 0px auto",
      }}
    >
      <Stack sx={{ px: "16px" }}>
        <Stack
          direction="row"
          justifyContent="space-between"
          alignItems="center"
        >
          <Typography variant="h5" sx={{ color: "#11305F" }}>
            Goal results
          </Typography>
          <Select
            size="small"
            value={"Monthly goal"}
            sx={{ color: "#1E1E1E", fontSize: "14px" }}
          >
            <MenuItem value={"Monthly goal"} sx={{ fontSize: "14px" }}>
              Monthly goal
            </MenuItem>
            <MenuItem value={"Year goal"} sx={{ fontSize: "14px" }}>
              Year goal
            </MenuItem>
          </Select>
        </Stack>
        <Stack
          direction="row"
          divider={<Divider />}
          justifyContent="space-between"
          mt={"20px"}
        >
          <Stack sx={{ width: "50%" }}>
            <Typography variant="body1" sx={{ color: "#587797" }}>
              Save
            </Typography>
            <Typography variant="h4" sx={{ color: "#14AE5C" }}>
              € {Math.round(saved)}
            </Typography>
          </Stack>
          <Stack sx={{ width: "50%" }}>
            <Typography variant="body1" sx={{ color: "#587797" }}>
              Current balance
            </Typography>
            <Typography variant="h4" sx={{ color: "#14AE5C" }}>
              € {total}
            </Typography>
          </Stack>
        </Stack>
        <Divider sx={{ my: "12px" }} />
        <Stack>
          <Typography variant="body1" sx={{ color: "#157FF7" }}>
            With completed goal: € {Math.round(total + saved)}
          </Typography>
        </Stack>
      </Stack>
    </Stack>
  );
}

type CategoryDetails = {
  name: string;
  description: string;
  chart: {
    current: number;
    goal: number;
  };
};

function Content({
  onSubmit,
  categoriesList,
  categoriesDetails,
  selectedCategories,
  setSelectedCategories,
}: {
  onSubmit: (value: string) => void;
  categoriesList: string[];
  categoriesDetails: CategoryDetails[];
  selectedCategories: CategoryDetails[];
  setSelectedCategories: (value: CategoryDetails[]) => void;
}) {
  const renderCategoriesDetails = useMemo(() => {
    return categoriesDetails.map((category) => (
      <CategoryOneCard
        {...category}
        key={category.name}
        isSelected={selectedCategories
          .map((item) => item.name)
          .includes(category.name)}
        onAddCategory={() => {
          setSelectedCategories([...selectedCategories, category]);
        }}
        onRemoveCategory={() => {
          setSelectedCategories(
            selectedCategories.filter((item) => item.name !== category.name)
          );
        }}
      />
    ));
  }, [categoriesDetails, selectedCategories, setSelectedCategories]);

  return (
    <Stack
      gap={"10px"}
      sx={{
        display: "flex",
        flexDirection: "column",
        justifyContent: "center",
        maxHeight: "calc(100vh - 320px)",
        width: "90%",
        overflow: "auto",
        margin: "auto auto 0px auto",
        overscrollBehavior: "contain",
      }}
    >
      <Stack gap={"10px"} sx={{ overflow: "auto", maxHeight: "100%" }}>
        {categoriesList.length > 0 && <CategoriesCard items={categoriesList} />}
        {renderCategoriesDetails}
      </Stack>
      <InputForm onSubmit={onSubmit} />
    </Stack>
  );
}

function InputForm({ onSubmit }: { onSubmit: (value: string) => void }) {
  const [value, setValue] = useState("");
  return (
    <Stack>
      <TextField
        sx={{
          border: "1px solid #EEF2F5",
          backgroundColor: "#fff",
        }}
        value={value}
        onChange={(e) => setValue(e.target.value)}
        multiline
        maxRows={4}
        slotProps={{
          input: {
            sx: { border: "none" },
            endAdornment: (
              <IconButton
                disabled={!value}
                onClick={() => onSubmit(value)}
                sx={{
                  background: "#EFF4FD",
                  color: "#1A65C7",
                  borderRadius: "6.4px",
                }}
              >
                <SendOutlinedIcon />
              </IconButton>
            ),
          },
        }}
      />
    </Stack>
  );
}

function CategoriesCard({ items }: { items: string[] }) {
  return (
    <Card>
      <Stack gap={"10px"}>
        <Typography fontSize={16} fontWeight={600}>
          Your secondary categories:
        </Typography>
        <Stack direction="row" gap={1} flexWrap="wrap">
          {items.map((item) => (
            <Chip
              key={item}
              label={item}
              color="info"
              deleteIcon={<ClearIcon />}
              onDelete={() => {}}
            />
          ))}
        </Stack>
      </Stack>
    </Card>
  );
}

function CategoryOneCard({
  name,
  description,
  chart,
  onAddCategory,
  isSelected,
  onRemoveCategory,
}: {
  name: string;
  description: string;
  chart: {
    current: number;
    goal: number;
  };
  onAddCategory: () => void;
  onRemoveCategory: () => void;
  isSelected: boolean;
}) {
  return (
    <Card>
      <Stack gap={"10px"}>
        <Typography fontSize={20} fontWeight={600}>
          We suggest you the plan for: {name}
        </Typography>
        <Typography>{description}</Typography>
        <PieChart
          series={[
            {
              data: [
                { id: 0, value: chart.goal, label: "Goal spends" },
                { id: 1, value: chart.current, label: "Current spends" },
              ],
            },
          ]}
          width={450}
          height={200}
        />
        {isSelected ? (
          <Stack direction="row" gap={2} alignItems="center">
            <Chip
              label="Added"
              variant="filled"
              color="success"
              sx={{ width: "fit-content", ml: "auto" }}
              avatar={<Check sx={{ color: "#fff !important" }} />}
            />
            <IconButton
              onClick={onRemoveCategory}
              color="error"
              sx={{
                borderRadius: "8px",
                background: "#FEE9E7",
              }}
            >
              <DeleteIcon />
            </IconButton>
          </Stack>
        ) : (
          <Button
            variant="contained"
            sx={{ width: "fit-content", ml: "auto" }}
            onClick={onAddCategory}
          >
            Add
          </Button>
        )}
      </Stack>
    </Card>
  );
}

function CategorySecondaryOneCard({
  name,
  description,
  chart,
}: {
  name: string;
  description: string;
  chart: {
    current: number;
  };
}) {
  return (
    <Card>
      <Stack gap={"10px"}>
        <Typography fontSize={20} fontWeight={600}>
          We suggest you the plan for: {name}
        </Typography>
        <Typography>{description}</Typography>
        <PieChart
          series={[
            {
              data: [{ id: 1, value: chart.current, label: "Current spends" }],
            },
          ]}
          width={450}
          height={200}
        />
        <Button variant="text" onClick={() => console.log("Clicked")}>
          Click to see more insights...
        </Button>
      </Stack>
    </Card>
  );
}

function MotivationCard({ text }: { text: string }) {
  return (
    <Card>
      <Stack gap={"10px"}>
        <Typography fontSize={20} fontWeight={600}>
          Motivation
        </Typography>
        <Typography>{text}</Typography>
      </Stack>
    </Card>
  );
}

const Card = styled(Stack)(() => ({
  borderRadius: "8px",
  boxShadow: " 0px 4px 30px 0px rgba(0, 0, 0, 0.04)",
  backgroundColor: "#fff",
  padding: "16px 16px 10px 16px",
}));

const Container = styled(Stack)(() => ({
  minHeight: "100dvh",
  maxWidth: "560px",
  width: "100%",
  backgroundColor: "#FBFBFB",
  display: "flex",
  flex: 1,
  paddingBottom: "20px",
  gap: "20px",
}));

const Page = styled(Stack)(() => ({
  display: "flex",
  alignItems: "center",
  justifyContent: "center",
  backgroundColor: "#212121",
  width: "100%",
  minHeight: "100dvh",
}));
